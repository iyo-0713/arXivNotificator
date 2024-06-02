# arXivNotifier

本プロジェクトではslackから毎日情報を取得し、ユーザの好みに合わせた論文の推薦をSlackとNotionをUIとして行います

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
### 1. **RepositoryのClone:**
    ```bash
    git clone https://github.com/iyo-0713/arXivNotificator.git
    cd arXivNotifier
    ```
### 2. **.envファイルの作成:**
    - Create a `.env` file in the root directory and add the necessary environment variables as shown below:
    ```env
    SLACK_BOT_TOKEN==your_slack_bot_token
    NOTION_INTEGRATION_TOKEN=your_notion_api_token
    NOTION_DATABASE_ID=your_notion_database_id
    TEMPLATE_PAGE_ID=your_notion_template_id
    OPENAI_API_key=your_openai_api_token

### 3. **Build and run the Docker container:**

    
### 4. **Build and run the Docker container:**
    Build the Docker image:
    ```bash
    docker build -t arxivnotifier .
    ```
    Run the Docker container:
    ```bash
    docker run -d --name arxivnotifier arxivnotifier
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

何かありましたら以下のアドレスまでご連絡ください
h.yasukawa.0713☆gmail.com
（☆を@に変える）











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

本プロジェクトでは

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

何かありましたら以下のアドレスまでご連絡ください
h.yasukawa.0713☆gmail.com
（☆を@に変える）
