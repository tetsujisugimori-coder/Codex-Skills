---
name: gh-review-merge-sync
description: チャットのレビューをcommit・pushして正式なSubmit reviewを行い、条件を満たす対象PRをmergeし、作業ブランチを削除して指定ローカルmainをfast-forward更新する。「レビュー提出からマージ・ブランチ削除・ローカルmainへpullまで」「レビュー提出・マージ・後片付け」を明示した依頼で使う。レビューだけ・投稿だけの依頼では起動しない。
---

# レビュー提出・マージ・後片付け
このスキルを明示して実行する依頼は、対象PRのレビュー記録・commit・push・Submit review・merge・対象作業ブランチ削除・指定ローカルmain更新を一連で許可する。通常は同じ許可を聞き直さず、以下の確認を行って進める。スキルを作成・インストールする依頼自体は実PR操作の許可ではない。今回の利用者の範囲指定を優先する。日本語で記録・報告する。

## 対象とレビューの確定
1. このチャットで利用者が提出を求めたレビュー本文、対象の owner/repo とPR番号を特定する。実装者の完了報告とレビュアーの評価を取り違えない。複数候補があり会話から一意に決まらない場合だけ確認する。関係ないPRを探索・変更しない。
2. GitHub接続と利用可能なローカル作業環境を確認する。外部操作には利用可能ならGitHubプラグインを優先し、不足する操作には認証済みCLIを使う。未提供のツール名や権限を想定しない。
3. PRのURL、OPEN/MERGED/CLOSED、Draft、base/headリポジトリ、base/headブランチ、最新HEAD、作者、接続アカウント、既存Reviewを取得する。対象プロジェクトのAGENTS.mdとレビュー保存規約を読む。
4. レビューが対象としたSHAをreviewed_sha、現在のHEADをobserved_headとして区別する。レビュー内にSHAがない場合、実際にその版を確認した証拠がなければ「対象版未特定・提示要約の評価」と記す。版を後付けで検証済み扱いにしない。
5. reviewed_sha以後に変更がある場合は差分を読み、レビューの有効範囲を判断する。変更された製品コードを未確認のまま最新HEADへのPASSやApproveに流用しない。過去版の評価は対象SHAと現時点の制限を明記して記録・Comment提出できる。
6. 原レビューの判定、優先度、根拠、未検証事項を忠実に保持する。「要約への評価」と「コード・証拠を直接検証した評価」を分け、未実施のテストや独立レビューを追加しない。公開先に秘密・個人情報を持ち込まない。

## レビューを記録してcommit・pushする
1. レビューは対象PRのheadブランチへ文書として記録する。既存規約を優先し、規約がなければ docs/reviews/pr-<番号>-<YYYYMMDD-HHmmss-JST>.md を使う。PRリンク、reviewed_sha、記録前HEAD、評価範囲、レビュー本文、JST作成日時を含める。ブランチを固定値で推測しない。
2. 同じレビューが既に保存・提出されていないか、ファイルとGitHub Reviewを照合する。保存済みなら再利用し、提出済みならリンクを報告する。途中失敗から再開しても不要な重複commit・Reviewを作らない。更新は追補で履歴を保持する。
3. ローカルでは対象remoteとheadを照合する。既存変更・index・別worktreeを保護し、必要なら清潔な別worktreeを作る。無関係な変更をstash・commit・破棄しない。PRブランチへの書込み権限がない場合、別PRやmainへの保存にすり替えない。
4. 文書内容と git diff --check を確認し、レビュー用ファイルだけを明示的にstageして日本語のメッセージでcommitする。git add .、force-push、reset --hard、clean、他人の変更を巻き込む操作をしない。製品コードやテストの修正はこのスキルの範囲に含めない。
5. 対象headブランチへ通常pushする。拒否時は最新状態を再取得し、並行変更を確認してから安全に再計画する。GitHub側の文書書込み機能でcommitできる場合も、branchを必ず明示して同等の検証をする。
6. 書込み後にGitHubからcommit、ファイル本文、最新HEADを読み戻す。レビュー文書のみの追加を確認し、submission_headを確定する。reviewed_shaとsubmission_headを混同しない。文書以外が動いたらレビュー範囲を再評価する。

## GitHubでSubmit reviewする
1. 通常のIssueコメントやPR本文の編集ではなく、正式なPull Request Reviewを提出する。GitHubプラグインでは add_review_to_pr を利用可能な定義から発見し、commit_idにsubmission_headを指定する。
2. 既定はCOMMENTとする。利用者がApproveまたはRequest changesを明示した場合のみ、実際の判定・検証範囲・アカウント権限と両立するイベントを選ぶ。自分が作者のPRに自己Approveや自己Request changesを試みない。その場合はCOMMENTで原判定を記し、レビュー承認の代替にはならないと報告する。
3. 本文には原レビュー、対象SHA、最新SHAとの差、保存文書へのcommit固定リンク、判定と制限を含め、末尾に現在の日本時間を入れる。チャット本文からGitHub Reviewへ転記するために内容を勝手に好意的に書き換えない。
4. 投稿直前にHEADを再取得し、変化したら提出内容・対象版を再確認する。APIに原子的HEAD条件がない提出では、投稿後にもHEADとreview.commit_idを確認し、競合があれば最新HEADの承認済み扱いにしない。
5. Review ID/URL、stateがPENDINGではなく提出済みであること、本文、commit_idを読み戻す。権限不足やAPI失敗を通常コメントで代替して「Submit review完了」と報告しない。成功済みのcommitを取り消さず、未完了の操作を明示する。

## 実行計画と再開
最初に全工程の利用可能性を確認し、利用者が使っているローカルcheckoutを会話と環境から特定する。新しく作ったクラウドcloneをWindows等の利用者ローカルmainの代わりとして報告しない。ローカルへ接続できない場合も独立して可能な工程を完了し、ローカルpullだけ未実施と明示する。
PRが既にMERGEDならheadへレビュー文書を追記するためにブランチを再作成しない。既存の保存・提出結果を照合し、未完了の後片付けから再開する。必要なレビュー記録が存在しなければ、マージ済みで記録工程未実施と報告し、別PRやmainへの直接commitにすり替えない。CLOSEDかつ未マージなら停止する。

## マージ条件の確認
1. 原レビューに未解決のP0〜P2、マージNO、HOLD、比較対象版の不明、必要範囲の未検証がある場合は自動的にPASSへ変更しない。既に明示された利用者の限定受入れ・例外判断があれば適用範囲を記し、それ以外はレビュー提出までを完了してマージを保留する。P3だけで機械的に停止しない。
2. レビュー記録commit後の最新submission_headについて、必要なCI/check/status、レビュー要件、未解決スレッド、mergeabilityを確認する。古いHEADのCIを流用しない。no checks reported、未実行、skipを成功と表現しない。CIがない構成でも利用者の受入条件とGitHub要件を満たすなら、その制限を記して進める。必須条件の充足が確認できなければ保留する。
3. pending中は短い待機と進捗報告で追跡する。無限待機しない。失敗時は原因を読み、レビュー文書の形式など今回の記録工程に起因する問題のみ局所修正できる。製品変更やテスト弱体化、保護ルール回避で成功させない。
4. Draftなら、このスキルの明示呼出しに含まれるマージ指示に基づき、条件確認後にReady for reviewへ変更できる。必要な別人のApproveを偽装しない。自己PRへのCOMMENTは承認要件を満たさない。
5. 再取得した最新HEADがsubmission_headと一致することを確認し、GitHubで有効な既存方針に従うmerge方式を選ぶ。可能ならexpected_head_sha付きのmerge_pull_requestを使い、CLIなら同等のHEAD一致条件を指定する。保護回避、admin bypass、force、auto-mergeで条件を迂回しない。
6. merged=true、merge commit SHA、merged_at、baseブランチをGitHubから読み戻して初めてマージ成功とする。HEAD移動で拒否された場合は変更を再確認し、古いレビューのまま再試行しない。マージ失敗時には削除へ進まない。

## ブランチ削除とローカルmain更新
1. マージ完了後、削除対象がこのPRのheadブランチで、main・default・release等の共有/保護ブランチでないことを確認する。forkのブランチは明示許可がなければ削除しない。マージ後に新しいcommitが追加されていないかremoteのrefと確定したheadを比較する。HEADが変わっていたら削除を保留する。
2. GitHubの設定で既に削除済みなら成功済みとして扱う。remote削除は利用可能なら期待する旧SHAを条件にしたref削除を用いる。通常の取得・削除しかできない場合は直前に再確認し、並行変更の疑いがあれば保存する。リモート削除結果を確認する。
3. 対象ローカルcheckoutのremote URL、作業ツリー、index、現在ブランチ、worktree一覧を確認する。汚れた作業ツリーを勝手にstash・commit・破棄しない。別の既存worktreeにmainがあれば、同じ対象repoであることとclean状態を確認してそちらを使う。作業ブランチのworktreeを強制削除しない。
4. origin/mainをfetchし、cleanな対象worktreeでmainへswitchする。mainがなければorigin/mainから追跡ブランチを作れる。git pull --ff-only origin main で更新する。baseがmainでないPRでは、mainへ統合済みと誤認せず、main更新とPRのmerge先を分けて報告する。
5. local mainに独自commitや分岐がある場合、reset・force・勝手なrebaseで揃えない。更新保留として保存する。更新後にmainのSHAと取得したorigin/mainのSHA、clean状態を確認する。後続pushでremoteが進んでいれば再fetchして比較し直す。
6. ローカル作業ブランチが他worktreeで使用中、未保存変更あり、マージ済みhead以外の独自commitありの場合は残す。mainに到達可能なら通常の branch -d を使う。squash/rebase mergeで到達不能でも、PRの実マージ・head一致・独自commitなし・未使用を確認した場合に限り、このPRブランチの削除指示に基づき branch -D を使える。必要な証拠が揃わなければ削除保留とする。
7. 利用可能なら既存pull-mainスキルの安全手順を参照できるが、この手順だけでも完結させる。main更新のためだけにアプリ全テスト、依存更新、別機能開発を開始しない。

## 最終報告
工程ごとに、レビュー記録commit/URL、Review URLとイベント、merge結果/URLとSHA、remote/localブランチ削除結果、実際のローカルパスとmain更新前後SHA、作業ツリー状態を簡潔に示す。成功・既に完了・保留・失敗・接続不能を区別し、どれか未完了なら「全工程完了」と言わない。末尾に現在の日本時間を付ける。
