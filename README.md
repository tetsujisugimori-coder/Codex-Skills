# Codex Skills
個人用Codexスキルの配布元です。Command Pocketから、導入依頼文と普段使う呼び出し文をコピーできます。

[Command Pocketを開く](https://tetsujisugimori-coder.github.io/Command-Pocket/)

## 収録スキル
| 名前 | 実行範囲 |
| --- | --- |
| gh-commit-submit-review | 作成済みレビューの記録・正式提出まで |
| gh-review-merge | レビュー提出・マージ・作業ブランチ削除まで。main更新なし |
| gh-review-merge-sync | 上記と指定ローカルmainのfast-forward更新 |
| pull-main | 現在のリポジトリのローカルmainを安全に更新 |
| failure-convergence-review | 破綻条件を探索し、証拠に基づきレビューを収束・マージ推奨まで判断 |
| root-cause-review | 難航問題の原因と過去の実装制約を再評価し、根本解決策を提案 |

各スキルの正本は `skills/<名前>/` です。初版の4スキルはChatGPT側の個人スキルから本文・表示設定・アイコンを収録しています。追加した2つのレビュースキルはChatGPTで作成したSKILL.mdを元に、このリポジトリ用の表示設定とアイコンを付けています。更新元間の自動同期はありません。今後の変更では、このリポジトリとChatGPT側のどちらを変更したかを区別し、Command Pocketの参照版も明示的に更新します。

## 初回導入
Command Pocketの「CLIにスキルを導入」から、対象を選んで「導入依頼文をコピー」。Codex CLIに貼り付けてください。ブラウザがPCへ直接インストールする機能ではありません。
依頼文はこのリポジトリの特定commitを指定し、manifest.jsonのSHA-256と照合して配置するようCLIへ指示します。PowerShellインストーラーや実行ポリシー変更は不要です。詳しくは [INSTALL.md](INSTALL.md) を参照してください。

## 導入後の呼び出し
CLIの `/skills` に表示されるか確認し、`$gh-review-merge` などを指定して依頼します。配置成功と認識成功は別々に確認します。スキルの導入だけでは実PRの投稿・マージ等を許可しません。
レビューを別チャットから持ち込む場合は、レビュー本文・対象PR・レビュー対象SHAも渡してください。

## 検証
```sh
python -m unittest discover -s tests
```
manifest.jsonに列挙した全ファイルのサイズとSHA-256、収録パスの範囲、スキル名と必須ファイルの整合を確認します。実PRの操作はテストしません。
