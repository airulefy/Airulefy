# CLIリファレンス

Airulefyは、コマンドラインインターフェース（CLI）を通じて操作できます。このページでは、
利用可能なすべてのコマンドとオプションについて説明します。

## 基本的な使用法

```bash
airulefy [オプション] [コマンド]
```

## グローバルオプション

| オプション | 説明 |
|----------|------|
| `--version` | バージョン情報を表示して終了します |
| `--help` | ヘルプメッセージを表示して終了します |

## コマンド一覧

### generate

AIルールファイルを生成します。

```bash
airulefy generate [オプション]
```

**オプション:**

| オプション | 説明 |
|----------|------|
| `--copy`, `-c` | シンボリックリンクの代わりにファイルをコピーします |
| `--verbose`, `-v` | 詳細な出力を表示します |
| `--preserve-structure`, `-p` | ディレクトリ構造を保持し、Cursor用に複数の.mdcファイルを出力 |
| `--help` | ヘルプメッセージを表示します |

**使用例:**

```bash
# デフォルトモード（設定に従う）でルールを生成
airulefy generate

# コピーモードでルールを生成
airulefy generate --copy

# 詳細出力付きでルールを生成
airulefy generate --verbose

# ディレクトリ構造を保持してCursor用のルールを生成
airulefy generate --preserve-structure
```

### watch

`.ai/`ディレクトリを監視し、変更があれば自動的にルールファイルを再生成します。

```bash
airulefy watch [オプション]
```

**オプション:**

| オプション | 説明 |
|----------|------|
| `--copy`, `-c` | シンボリックリンクの代わりにファイルをコピーします |
| `--preserve-structure`, `-p` | ディレクトリ構造を保持し、Cursor用に複数の.mdcファイルを出力 |
| `--help` | ヘルプメッセージを表示します |

**使用例:**

```bash
# デフォルトモードで変更を監視
airulefy watch

# コピーモードで変更を監視
airulefy watch --copy

# ディレクトリ構造を保持してCursor用の変更を監視
airulefy watch --preserve-structure
```

### validate

設定とルールファイルを検証します。

```bash
airulefy validate
```

**オプション:**

| オプション | 説明 |
|----------|------|
| `--help` | ヘルプメッセージを表示します |

**使用例:**

```bash
airulefy validate
```

### list-tools

サポートされているAIツールとその設定を一覧表示します。

```bash
airulefy list-tools
```

**オプション:**

| オプション | 説明 |
|----------|------|
| `--help` | ヘルプメッセージを表示します |

**使用例:**

```bash
airulefy list-tools
```

## 終了コード

| コード | 説明 |
|------|------|
| 0 | 成功 |
| 1 | エラー/失敗 |
