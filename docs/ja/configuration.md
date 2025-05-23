# 設定方法

Airulefyの動作は、`.ai-rules.yml`設定ファイルを通じてカスタマイズできます。
このページでは、利用可能なすべての設定オプションと使用例について説明します。

## 基本設定

設定ファイルは、プロジェクトのルートディレクトリに`.ai-rules.yml`という名前で作成します。
基本的な設定例：

```yaml
default_mode: symlink
input_path: .ai
tools:
  cursor: {}
  cline: {}
  copilot: {}
  devin: {}
```

## 設定オプション

### グローバル設定

| オプション | 説明 | デフォルト値 | 有効な値 |
|----------|------|------------|---------|
| `default_mode` | デフォルトの同期モード | `symlink` | `symlink`, `copy` |
| `input_path` | AIルールファイルを含むディレクトリのパス | `.ai` | 任意の相対パス |

### ツール固有の設定

各ツールには以下のオプションが設定可能です：

| オプション | 説明 | デフォルト値 | 有効な値 |
|----------|------|------------|---------|
| `mode` | このツール用の同期モード | `default_mode`の値 | `symlink`, `copy` |
| `output` | 出力ファイルのパス | ツールによる | 任意の相対パス |

## サポートされているツールとデフォルト出力先

| ツール名 | デフォルト出力先 |
|--------|---------------|
| `cursor` | `.cursor/rules/core.mdc` |
| `cline` | `.cline-rules` |
| `copilot` | `.github/copilot-instructions.md` |
| `devin` | `devin-guidelines.md` |

## 設定例

### シンプルな設定

```yaml
default_mode: symlink
```

すべてのツールでシンボリックリンクを使用し、デフォルトの出力先を使用します。

### ツール固有の出力先

```yaml
default_mode: symlink
tools:
  cursor:
    output: ".cursor/rules/project-rules.mdc"
  devin:
    output: "docs/devin-instructions.md"
```

Cursorと Devinの出力先をカスタマイズします。

### 混合モード

```yaml
default_mode: symlink
tools:
  cursor: {}  # シンボリックリンクを使用
  cline:
    mode: copy  # コピーを使用
  copilot:
    mode: symlink  # 明示的にシンボリックリンクを指定
  devin:
    mode: copy  # コピーを使用
    output: "custom/path/devin-guide.md"  # カスタム出力先
```

ツールごとに異なる同期モードと出力先を指定します。

### カスタム入力パス

```yaml
default_mode: symlink
input_path: "docs/ai-rules"
```

AIルールファイルを`.ai`ディレクトリではなく`docs/ai-rules`ディレクトリから読み込みます。

## 注意事項

- `symlink`モードはWindows上で管理者権限が必要な場合があります
- 一部の環境ではシンボリックリンクがサポートされていない場合、自動的に`copy`モードが使用されます
- ファイルが存在しない場合に限り出力ディレクトリが自動的に作成されます
