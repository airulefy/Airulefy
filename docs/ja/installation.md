# インストール方法

Airulefyは、さまざまな方法でインストールできます。自分の環境や好みに合った方法を選んでください。

## 前提条件

- Python 3.11以上
- pip または Poetry（推奨）

## Poetryを使用したインストール（推奨）

[Poetry](https://python-poetry.org/)は、依存関係管理と環境の分離を容易にする現代的なPythonパッケージマネージャーです。

```bash
# Poetryがまだインストールされていない場合
curl -sSL https://install.python-poetry.org | python3 -

# Airulefyをインストール
poetry add airulefy
```

既存のプロジェクトに開発依存関係としてインストールする場合：

```bash
poetry add --dev airulefy
```

## pipを使用したインストール

標準的なPythonパッケージマネージャーを使用してインストールします：

```bash
pip install airulefy
```

特定のバージョンをインストールしたい場合：

```bash
pip install airulefy==0.1.0
```

## DevContainerを使用したセットアップ

VSCodeのDevContainerを使用している場合、簡単に環境をセットアップできます：

1. `.devcontainer/devcontainer.json`ファイルに以下を追加します：

```json
{
  "name": "Python Development",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "postCreateCommand": "pip install airulefy",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python"
      ]
    }
  }
}
```

2. DevContainerを再起動すると、Airulefyが自動的にインストールされます。

## GitHub Codespacesでの使用

GitHub Codespacesを使用している場合：

1. リポジトリにDevContainer設定を含めます（上記参照）
2. Codespacesを起動すると、Airulefyが自動的にインストールされます
3. あるいは、Codespacesのターミナルで直接インストールすることも可能です：

```bash
pip install airulefy
```
