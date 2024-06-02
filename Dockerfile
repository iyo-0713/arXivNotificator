# ベースイメージを指定
FROM python:3.9-slim

# cronをインストール
RUN apt-get update && apt-get install -y cron python3-pip

# 作業ディレクトリを設定
WORKDIR /app

# 必要なPythonパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードとデータファイルをコピー
COPY src/ src/
COPY data/ data/
COPY config.json config.json
COPY .env .env

# cronジョブを設定
COPY crontab /etc/cron.d/my-cron-job
RUN chmod 0644 /etc/cron.d/my-cron-job
RUN crontab /etc/cron.d/my-cron-job

# cronデーモンとPythonスクリプトを実行
CMD ["cron", "-f"]