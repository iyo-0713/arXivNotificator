# arXivNotifier

This project collects information from arXiv periodically and notifies it to Notion and Slack.

## Directory Structure

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

1. **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/arXivNotifier.git
    cd arXivNotifier
    ```

2. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the environment variables:**
    - Create a `.env` file in the root directory and add the necessary environment variables as shown below:
    ```env
    SLACK_BOT_TOKEN==your_slack_bot_token
    NOTION_INTEGRATION_TOKEN=your_notion_api_token
    NOTION_DATABASE_ID=your_notion_database_id
    TEMPLATE_PAGE_ID=your_notion_template_id
    OPENAI_API_key=your_openai_api_token
    ```

### Configuration

Edit the `config.json` file to customize the notification settings and other configurations.

### API Usage
This project uses the following APIs:

# TODO APIのリンクを調べる

OpenAI API
Slack API
Notion API
arXiv API

Please ensure compliance with each API's usage policies and terms of service.

### Contact

For any inquiries, please contact [your_email@example.com].












## Usage

To start the notifier, run:
```bash
python src/main.py
```

## Configuration

Edit the `config.json` file to customize the notification settings and other configurations.

## Docker

To run the project using Docker:

1. **Build the Docker image:**
    ```bash
    docker build -t arxivnotifier .
    ```

2. **Run the Docker container:**
    ```bash
    docker run --env-file .env arxivnotifier
    ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any inquiries, please contact [your_email@example.com].
```

### 各セクションの説明

1. **プロジェクトのタイトルと概要**
   - プロジェクト名とその目的を簡潔に説明します。

2. **ディレクトリ構造**
   - プロジェクトのファイル構造を示します。これにより、ユーザーはどのファイルがどの機能に関連しているかを理解しやすくなります。

3. **インストール方法**
   - プロジェクトをクローンし、必要な依存関係をインストールする手順を示します。

4. **使用方法**
   - プロジェクトの実行方法を説明します。

5. **環境変数の設定**
   - プロジェクトで必要な環境変数の設定方法を示します。

6. **ライセンス**
   - プロジェクトのライセンス情報を記載します。

7. **連絡先情報**
   - 問い合わせ先の情報を提供します（オプション）。

8. **貢献ガイドライン**
   - プロジェクトへの貢献方法についてのガイドラインを提供します（オプション）。

README.mdを作成することで、プロジェクトの利用者がインストールや使用方法を理解しやすくなります。何か他に質問があれば教えてください。