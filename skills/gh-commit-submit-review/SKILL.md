---
name: gh-commit-submit-review
description: チャットで作成済みのレビューを対象GitHub PRへ文書としてcommit・pushし、正式なSubmit reviewを行う。「このレビューをcommitしてsubmit review」「レビュー記録・提出」の依頼で使う。提出で終了し、マージ、Draft解除、ブランチ削除、main更新は行わない。レビュー依頼だけでは外部投稿を開始しない。
---

# レビュー記録・提出
利用者が指定したチャットのレビューを、対象PRへ記録して正式なReviewとして提出する。このスキルの呼出しはレビュー保存・commit・push・Review提出を許可する。作成・インストールを頼まれただけのときは実PRを操作しない。日本語で記録・報告する。

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

## 終了条件
提出後に停止する。Draft解除、マージ、auto-merge、ブランチ削除、main更新を実施しない。
レビュー文書とcommitへのリンク、Review URL、reviewed_shaとsubmission_head、提出イベント、PRが未マージであることを簡潔に報告する。未完了がある場合は工程別に明記する。報告末尾に日本時間を付ける。
