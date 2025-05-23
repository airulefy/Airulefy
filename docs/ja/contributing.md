# 貢献ガイド

Airulefyプロジェクトへの貢献に興味をお持ちいただき、ありがとうございます！このガイドでは、
開発環境のセットアップから、プルリクエストの作成、コーディング規約などについて説明します。

## 開発環境のセットアップ

### 必要条件

- Python 3.11以上
- Poetry（パッケージ管理用）
- Git

### 環境構築手順

1. リポジトリをクローンします：

```bash
git clone https://github.com/airulefy/Airulefy.git
cd Airulefy
```

2. Poetryを使って依存関係をインストールします：

```bash
# Poetryがまだインストールされていない場合
curl -sSL https://install.python-poetry.org | python3 -

# 依存関係をインストール
poetry install
```

3. pre-commitフックをインストールします：

```bash
poetry run pre-commit install
```

### DevContainerを使用する場合

VS Codeとその拡張機能を使用する場合は、DevContainerを使って開発環境を簡単にセットアップできます：

1. リポジトリをクローンした後、VS Codeで開きます：

```bash
git clone https://github.com/airulefy/Airulefy.git
code Airulefy
```

2. VS Codeが`.devcontainer`フォルダを検出したら、「Reopen in Container」を選択します。

詳細は[DevContainerドキュメント](./devcontainer.md)を参照してください。

## 開発ワークフロー

### ブランチ戦略

- `main`: リリース済みコード
- `develop`: 開発中のコード
- 機能ブランチ: `feature/xxxx`
- バグ修正ブランチ: `fix/xxxx`

### 新機能の追加またはバグ修正

1. 最新の`develop`ブランチから新しいブランチを作成します：

```bash
git checkout develop
git pull
git checkout -b feature/your-feature-name
```

2. 変更を実装します。

3. テストを追加または更新し、全てのテストがパスすることを確認します：

```bash
poetry run pytest
```

4. コードをフォーマットし、リンターを実行します：

```bash
poetry run black .
poetry run isort .
poetry run mypy .
```

5. 変更をコミットします（[Conventional Commits](#conventional-commits)の形式に従ってください）：

```bash
git add .
git commit -m "feat: add new feature X"
```

6. 変更をプッシュします：

```bash
git push -u origin feature/your-feature-name
```

7. GitHubでプルリクエストを作成し、`develop`ブランチをターゲットにします。

## テスト

Airulefyでは、pytest を使用してテストを実行します：

```bash
# すべてのテストを実行
poetry run pytest

# カバレッジレポートを生成
poetry run pytest --cov=airulefy

# 特定のテストファイルを実行
poetry run pytest tests/test_cli.py
```

すべての新機能には対応するテストを追加し、既存の機能を変更する場合は関連するテストを更新してください。

## コーディング規約

### Pythonスタイルガイド

- [PEP 8](https://www.python.org/dev/peps/pep-0008/)に従ってください
- [black](https://black.readthedocs.io/)と[isort](https://pycqa.github.io/isort/)を使用して自動フォーマット
- [mypy](http://mypy-lang.org/)を使用して型チェック

### ドキュメント

- すべての公開関数、クラス、メソッドにはdocstringを追加してください
- [Google スタイルのdocstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)を使用してください

### <a name="conventional-commits"></a>Conventional Commits

コミットメッセージは[Conventional Commits](https://www.conventionalcommits.org/)の形式に従ってください：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

タイプには以下があります：

- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの意味に影響しない変更（空白、フォーマット、セミコロンの欠落など）
- `refactor`: バグ修正でも新機能追加でもないコード変更
- `perf`: パフォーマンスを向上させるコード変更
- `test`: 不足しているテストの追加または既存のテストの修正
- `chore`: ビルドプロセスまたは補助ツールとライブラリの変更

例：

```
feat: 監視モードに自動再接続機能を追加

接続が切れた場合、30秒ごとに再接続を試みるようになりました。
これにより長時間の運用中の信頼性が向上します。

Fixes #123
```

## プルリクエスト

プルリクエストを送信する前に：

1. コードがすべてのテストをパスすることを確認
2. コードが適切にフォーマットされていることを確認
3. 必要に応じてドキュメントを更新
4. プルリクエストに変更内容の詳細な説明を含める

## リリースプロセス

Airulefyのリリースは以下のステップで行われます：

1. `develop`ブランチで全てのテストが成功することを確認
2. バージョン番号を更新（`pyproject.toml`）
3. CHANGELOGの更新
4. `main`ブランチにマージ
5. リリースタグの作成
6. PyPIへの公開

## 質問がある場合

質問や懸念がある場合は、GitHubのIssueセクションで新しいIssueを作成してください。
私たちはできるだけ早く対応します。

ご貢献をお待ちしています！
