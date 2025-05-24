# クイックスタート

Airulefyの基本的な使い方を5分で習得できるクイックスタートガイドです。

## 1. プロジェクトの準備

まず、AIルール用のディレクトリを作成します：

```bash
# プロジェクトのルートディレクトリで
mkdir -p .ai
```

## 2. AIルールファイルの作成

`.ai`ディレクトリにMarkdownファイルを作成します：

```bash
cat > .ai/main.md << EOL
# プロジェクトルール

このプロジェクトでは以下のコーディング規約に従ってください：

## コード規約
- インデントにはスペースを使用（タブではなく）
- 変数名はキャメルケースで
- 関数名はスネークケースで
- コメントは日本語で記述

## エラーハンドリング
- 例外は適切に捕捉すること
- 例外はログに記録すること
EOL
```

必要に応じて追加のルールファイルを作成できます：

```bash
cat > .ai/architecture.md << EOL
# アーキテクチャガイドライン

## レイヤードアーキテクチャ
このプロジェクトでは以下のレイヤーに従ってください：
- プレゼンテーション層
- ビジネスロジック層
- データアクセス層
EOL
```

## 3. 設定ファイルの作成（オプション）

必要に応じて、`.ai-rules.yml`設定ファイルを作成できます：

```bash
cat > .ai-rules.yml << EOL
default_mode: symlink
tools:
  cursor:
    output: ".cursor/rules/core.mdc"
  cline:
    mode: copy
  copilot: {}
  devin:
    output: "devin-guidelines.md"
EOL
```

## 4. AIルールの生成

設定したAIルールを各ツール用に生成します：

```bash
airulefy generate
```

出力例：

```
Successfully generated rule files:
- .cursor/rules/core.mdc [symlink]
- .cline-rules [copy]
- .github/copilot-instructions.md [symlink]
- devin-guidelines.md [symlink]
```

詳細出力を表示するには `-v` オプションを使用します：

```bash
airulefy generate -v
```

ディレクトリ構造を保持したいCursorユーザーの場合：

```bash
airulefy generate --preserve-structure
```

これにより、`.ai/`の元のディレクトリ構造を保持したまま、`.cursor/rules/`に複数の`.mdc`ファイルが生成されます。

## 5. 変更監視モード（オプション）

`.ai`ディレクトリの変更を監視し、変更があれば自動的にルールを再生成するモードを実行できます：

```bash
airulefy watch
```

これにより、ルールファイルを編集するたびに、各AIツール用のファイルが自動的に更新されます。

## 6. サポートされているツールの一覧表示

サポートされているAIツールとその設定を確認するには：

```bash
airulefy list-tools
```

## 7. 設定の検証

現在の設定とルールファイルを検証するには：

```bash
airulefy validate
```
