# arXivNotificator

本プロジェクトではarXivから毎日情報を取得し、ユーザの好みに合わせた論文の推薦をSlackとNotionをUIとして行います。

なお推薦は、arXivから取得した論文からOpenAI APIを用いて埋め込み表現を取得し、notionに記録された論文とどの程度類似しているかに準じています。

詳細は以下のブログを参考にしてください。

## Directory Structure
```
arXivNotificator/
├── data/
│   ├── log/
│   └── initial_data.json
├── src/
│   ├── __pycache__/
│   ├── arxiv_api.py
│   ├── main.py
│   ├── notion_api.py
│   ├── openai_api.py
│   ├── slack_api.py
│   └── utils.py
├── .env
├── config.json
├── crontab
├── Dockerfile
├── README.md
└── requirements.txt
```

## Installation
### 1. **本リポジトリのClone:**

    git clone https://github.com/iyo-0713/arXivNotificator.git
    cd arXivNotifier

### 2. **.envファイルの作成:**
以下の環境変数を登録した'.env'ファイルをrootディレクトリに作成してください

    SLACK_BOT_TOKEN==your_slack_bot_token
    NOTION_INTEGRATION_TOKEN=your_notion_api_token
    NOTION_DATABASE_ID=your_notion_database_id
    TEMPLATE_PAGE_ID=your_notion_template_id (optional)
    OPENAI_API_key=your_openai_api_token

**Environment Variables**

- SLACK_BOT_TOKEN：通知を行うslack workspaceのUser OAuth token。slackへのメッセージ送信の認証に使われます
- NOTION_INTEGRATION_TOKEN：結果を記録するNotionのインテグレーションのtoken。Notionのworkspaceへのアクセスの認証に使われます
- NOTION_DATABASE_ID： 論文などの管理を行っているデータビューのID
- TEMPLATE_PAGE_ID (optional)：論文などの管理を行っているデータビューのテンプレートのID
- OPENAI_API_KEY: OpenAIのAPIにアクセスするためのAPI Key。OpenAIサービスとのやり取りのために使われます


### 3. **config.jsonの設定:**

以下の要素を持つconfig.jsonをご自身の目的に応じて編集してください
- keywords：arXivから取得した論文のフィルタリングに用いるキーワード。登録されている場合、そのキーワードを**含まない**論文は弾かれます
- slack_channel：通知を行うslackのチャンネル名
- add_to_notion：True/False。Notionとの連携ができない場合はFalseにしてください
- arxiv_to_notion：Notionに記録する論文の数
- arxiv_to_slack：Slackに通知する論文の数
- notion_title：Notionのデータビューにおいて、論文のタイトルを入れる項目名
- notion_url：Notionのデータビューにおいて、論文のリンクを入れる項目名
- initial_data_path：Notionのデータベースがない場合に利用するjsonファイルのパス。既存のNotionデータベースがない場合に、これまで読んだ論文のタイトルとリンクを配置したjsonファイルを作成し、参照してください

### 4. **crontabの設定(optional):**

推薦の定期実行はcronを用いて行っています。
デフォルトでは7:30に通知する設定にしていますが、時間を変える場合は以下のcrontabファイルを編集してください

    30 22 * * * /usr/local/bin/python3 /app/src/main.py >> /app/data/log/cron.log 2>&1


### 5. **Dockerコンテナのセットアップ:**

Docker imageのbuild:

    docker build -t arxiv-notificator .

Docker containerのrun:

    docker run -d --name arxiv-notificator arxiv-notificator

## API利用

本プロジェクトでは以下のAPIを利用しています。
本プロジェクトの利用の際には、各APIの利用規約を遵守してください

- [arXiv API](https://info.arxiv.org/help/api/index.html)
- [Slack API](https://api.slack.com/lang/ja-jp)
- [Notion API](https://developers.notion.com/)
- [OpenAI API](https://openai.com/index/openai-api/)

## Contact

何かありましたら以下のアドレスまでご連絡ください

    h.yasukawa.0713☆gmail.com（☆を@に変える）
