FROM python:3.11

# 作業ディレクトリの設定
WORKDIR /app

# requirements.txtをコピーして必要なパッケージをインストール
COPY requirements.txt .

# 必要に応じて、Pythonパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
