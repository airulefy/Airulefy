# Airulefy

![PyPI](https://img.shields.io/pypi/v/airulefy)
![License](https://img.shields.io/github/license/airulefy/Airulefy)

**AIルールを統一。1つのソースから、主要なAIコーディングエージェント全てに同期。**

Airulefyは、`.ai/`ディレクトリに単一のルールセットを維持し、各ツール固有の形式（Cursor、
Copilot、Cline、Devinなど）に自動的に生成またはリンクするのを容易にします。
コピー＆ペーストは不要。一貫性のない動作も解消されます。

## 主な機能

- プロジェクト全体のAIルール（Markdown）のための統一された`.ai/`フォルダ
- 自動生成:
  - `.cursor/rules/*.mdc`
  - `.cline-rules`
  - `.github/copilot-instructions.md`
  - `devin-guidelines.md`
- シンボリックリンクまたはコピーモード（OSの機能を自動検出）
- オプションのYAML設定: `.ai-rules.yml`
- CIおよびpre-commitフックとの連携

## なぜAirulefyが必要か

AI駆動の開発ツールが普及するにつれて、各ツールは独自のフォーマットと場所で指示を受け取ります。
これにより、複数のツールを使用する場合、同じ指示を何度も更新する必要があり、メンテナンスが
困難になります。

Airulefyは、単一の信頼できる情報源から各AIツールに必要な形式でファイルを自動的に生成または
リンクすることで、この問題を解決します。
