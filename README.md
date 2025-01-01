# 開発環境の作成手順
``` sh
docker-compose up -d
```
フロントエンドのフォルダーで以下を実行
```sh
npm i && npm run dev
```

# デプロイ時の手順
フロントエンドのフォルダーで以下を実行
```sh
npm run build
```
distディレクトリに静的ファイルが生成される AWS Amplifyに入れる

よくわかんないけどlamdaかec2にaiのコンテナをデプロイする
