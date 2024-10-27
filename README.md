# 環境構築
~/.zshrc または ~/.bashrc を開いて以下のコードを追加することで ./vendor/bin/sailを sailに短縮することができます。(※macやlinuxでのみ使えます。windowsの場合はwsl2などの仮想linuxで使用できます。)

    alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'

以下./vendor/bin/sailはsailと記載します。

インストールしたいディレクトリまで行って下記のコマンドを実行

    git clone "URL"
    cd dogorcat
    sail up -d
    sail artisan migrate
	sail npm install
	sail npm run dev

画面を開いてみましょう。
http://localhost/

## 設計
このプロジェクトは3つのコンテナで成り立っています。**データベース Laravel(web) RestAPI(AI)** RestAPIはport5000で起動しているので、 http://localhost:5000/　でアクセスできます。
RestAPIは**ai-rest**というフォルダーがコンテナと共有されているため、その中の書き換えればRestAPIへ反映されます。

必要であればai-rest内のDockerfileやdocker-composeを変更して独自にカスタマイズできます。

## プルリクとマージ
何かの機能をつくる場合はプロジェクトからissueを発行して、main->**feature/[issueid]** でgitのブランチを発行してください。

例：
issue#**1** 画像を受け取る処理
main -> feature/**1** (ブランチを発行)

次に機能を作り終えたら十分にバグがないかを確認して、feature->developにプルリクエストを発行してください

次にdevelopで動作確認して develop->mainにマージされます。
