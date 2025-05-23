# DevContainer

Airulefyは、Visual Studio CodeのDevContainerをサポートしており、開発環境を簡単にセットアップ
できます。このページでは、DevContainerの設定と使用方法について説明します。

## DevContainerとは

DevContainerはVS Codeの機能で、Dockerコンテナ内に完全な開発環境を構築できます。
これにより、どの開発者も同じ設定、ツール、拡張機能を持つ一貫した環境で作業できます。

## Airulefyの開発環境

Airulefyプロジェクトは、以下の特徴を持つDevContainer設定を提供しています：

- Python 3.11環境
- PoetryによるPythonパッケージ管理
- 自動テスト実行
- コード品質ツール（black、isort、mypy）の事前インストール
- VS Code Python拡張機能の自動設定

## devcontainer.json

`.devcontainer/devcontainer.json`ファイルは、DevContainerの主な設定ファイルです。
Airulefyで使用される設定の例：

```json
{
    "name": "Airulefy Development",
    "dockerFile": "Dockerfile",
    "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": false,
        "python.linting.mypyEnabled": true,
        "python.formatting.provider": "black",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    },
    "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "njpwerner.autodocstring"
    ],
    "postCreateCommand": "poetry install && pre-commit install",
    "remoteUser": "vscode"
}
```

## Dockerfile

`.devcontainer/Dockerfile`はDevContainerの基本イメージと追加のセットアップ手順を定義します：

```Dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.11

# Poetry環境変数
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Poetryのインストール
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry --version

# 必要なシステムパッケージのインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ワーキングディレクトリの設定
WORKDIR /workspaces/Airulefy
```

## 自動テスト実行

Airulefyの開発環境では、背景でテストを自動的に実行するように設定されています。
これは、`.vscode/settings.json`で以下のように設定されています：

```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.testing.autoTestDiscoverOnSaveEnabled": true
}
```

これにより、ファイルを保存するたびに関連するテストが自動的に実行されます。

## 開発コンテナの使用方法

1. Visual Studio Codeと[Remote - Containers拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)をインストール

2. Airulefyリポジトリをクローン：
   ```bash
   git clone https://github.com/airulefy/Airulefy.git
   cd Airulefy
   ```

3. VS Codeでフォルダを開く：
   ```bash
   code .
   ```

4. VS Codeが`.devcontainer`フォルダを検出し、通知を表示するので「Reopen in Container」を選択

5. コンテナのビルドと設定が完了するのを待ちます（初回は数分かかる場合があります）

6. これで、完全にセットアップされた開発環境でAirulefyの開発を開始できます！

## トラブルシューティング

### コンテナの再ビルド

依存関係が変わった場合など、コンテナを再ビルドする必要がある場合：

1. VS Codeコマンドパレットを開く（`Ctrl+Shift+P`または`Cmd+Shift+P`）
2. 「Remote-Containers: Rebuild Container」を選択

### ポートの転送

コンテナ内で実行されているサービスにアクセスするには、ポート転送を使用します。
VS Codeは自動的に多くのポートを検出しますが、手動で追加することも可能です：

1. VS Codeコマンドパレットを開く
2. 「Remote-Containers: Forward Port from Container」を選択
3. 転送したいポート番号を入力
