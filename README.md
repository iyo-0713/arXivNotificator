# arXivNotifier

本プロジェクトではslackから毎日情報を取得し、ユーザの好みに合わせた論文の推薦をSlackとNotionをUIとして行います。
詳細は以下のブログを参考にしてください。

## Directory Structure
```
arXivNotifier/
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
└── requirements.txt
```

## Installation
### 1. **本リポジトリのClone：**
    ```
    bash
    git clone https://github.com/iyo-0713/arXivNotificator.git
    cd arXivNotifier
    ```
### 2. **.envファイルの作成：**
    以下の環境変数を登録した'.env'ファイルをrootディレクトリに作成してください
    ```env
    SLACK_BOT_TOKEN==your_slack_bot_token
    NOTION_INTEGRATION_TOKEN=your_notion_api_token
    NOTION_DATABASE_ID=your_notion_database_id
    TEMPLATE_PAGE_ID=your_notion_template_id (optional)
    OPENAI_API_key=your_openai_api_token
    ```
    
    **Environment Variables**
    SLACK_BOT_TOKEN：通知を行うslack workspaceのUser OAuth token。slackへのメッセージ送信の認証に使われます
    NOTION_INTEGRATION_TOKEN：結果を記録するNotionのインテグレーションのtoken。Notionのworkspaceへのアクセスの認証に使われます
    NOTION_DATABASE_ID： 論文などの管理を行っているデータビューのID
    TEMPLATE_PAGE_ID (optional)：論文の管理を行っているデータビューのテンプレートのID
    OPENAI_API_KEY: OpenAIのAPIにアクセスするためAPI Key。OpenAIサービスとのやり取りのために使われます
    The API key for accessing the OpenAI API. This is used to interact with OpenAI services.

### 3. **config.jsonの設定:**
    以下の要素を持つconfig.jsonを作成してください
    keywords: List of keywords to filter arXiv papers. This should be a list of strings.
    slack_channel: The Slack channel where paper notifications will be sent.
    add_to_notion: Boolean flag to enable or disable adding notifications to Notion.
    arxiv_to_notion: Number of arXiv papers to add to Notion.
    arxiv_to_slack: Number of arXiv papers to send to Slack.
    notion_title: The title field used in Notion entries.
    notion_url: The URL field used in Notion entries.
    initial_data_path: Path to the initial data file used by the application.

### 4. **Build and run the Docker container:**
    Build the Docker image:
    ```bash
    docker build -t arxivnotifier .
    ```
    Run the Docker container:
    ```bash
    docker run -d --name arxivnotifier arxivnotifier
    ```

## API Usage
本プロジェクトでは以下のAPIを利用しています。

# TODO APIのリンクを調べる

OpenAI API
[Slack API](https://api.slack.com/lang/ja-jp)
[Notion API](https://developers.notion.com/)
arXiv API

Please ensure compliance with each API's usage policies and terms of service.

### Contact

何かありましたら以下のアドレスまでご連絡ください
h.yasukawa.0713☆gmail.com
（☆を@に変える）











何かありましたら以下のアドレスまでご連絡ください
h.yasukawa.0713☆gmail.com
（☆を@に変える）
