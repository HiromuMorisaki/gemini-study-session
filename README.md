# gemini-study-session
# Simple Error Log Analyzer

https://github.com/HiromuMorisaki/gemini-study-session.git

`access.log` から `ERROR` レベルのログを抽出し、エラーの種類ごとの発生回数と時間帯別の発生傾向を集計する、自己完結型のPythonスクリプトです。

## 🚀 特徴 (Features)

* **自己完結型:** 解析対象のログファイルが存在しない場合、テスト用のダミーログ（100行程度）を自動生成します。
* **エラー集計:** エラーメッセージの種類ごとに発生回数をカウントし、頻度を把握できます。
* **トレンド分析:** エラーの発生時間帯を1時間単位で集計し、障害の発生傾向を可視化します。
* **見やすい出力:** 実行結果はコンソールにMarkdown形式の表として出力されるため、レポート等へのコピペも容易です。
* **クリーンコード:** Type Hints（型ヒント）とDocstringを完備しており、チーム開発での再利用や学習用サンプルとしても最適です。標準ライブラリのみで動作します。

## 🛠 使い方 (Usage)

外部ライブラリ（`pip install`）は不要です。Python 3.x環境があればすぐに実行できます。

```bash
# 1. リポジトリをクローンしてディレクトリに移動
$git clone [https://github.com/HiromuMorisaki/gemini-study-session.git$](https://github.com/HiromuMorisaki/gemini-study-session.git$) cd gemini-study-session

# 2. スクリプトを実行
$ python log_analyzer.py
