#!/usr/bin/env python3
import requests
import os
import json
from dotenv import load_dotenv
from utils import load_config
load_dotenv('/app/.env')

# Notionに関する設定
NOTION_API_TOKEN = os.environ["NOTION_INTEGRATION_TOKEN"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]
try:
    TEMPLATE_PAGE_ID = os.environ["TEMPLATE_PAGE_ID"]
except KeyError:
    TEMPLATE_PAGE_ID = None

headers = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}
notion_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

def get_notion_data(url, headers):
    """
    Notion APIからデータベース情報を取得する。
    """
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        assert False, f"Failed to retrieve database: {e}"

def extract_notion_data(data):
    """
    Notionデータをクリーンアップし、必要な情報を抽出する。
    """
    if not data:
        return []
    cleaned_data = []
    # タイトル及びリンクのカラム名
    # デフォルトではNotionのデフォルト値を使用
    title_key = load_config().get('notion_title', "名前")
    link_key = load_config().get('notion_url', "URL")
    for result in data["results"]:
        title = result["properties"][title_key]["title"][0]["plain_text"]
        link = result["properties"][link_key]["url"]
        cleaned_data.append({"title": title, "link": link})
    return cleaned_data

# できればテンプレートの指定があるかどうかで考える
def load_template_data():
    # テンプレートページの内容を取得
    template_url = f"https://api.notion.com/v1/blocks/{TEMPLATE_PAGE_ID}/children"
    try:
        template_response = requests.get(template_url, headers=headers)
        template_response.raise_for_status()  # HTTPエラーが発生した場合に例外を発生させる
        template_content = template_response.json()
        template_blocks = template_content.get('results', None)
        return template_blocks
    except requests.exceptions.RequestException as e:
        print(f"Error fetching template data: {e}")
        return None
    
def add_to_notion(page_data):
    template_blocks = load_template_data()

    # ページを作成
    page_response = requests.post("https://api.notion.com/v1/pages", headers=headers, data=json.dumps(page_data))
    page = page_response.json()
    page_id = page['id']

    if template_blocks is not None:
        # テンプレート内容を新しいページに追加
        block_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        block_data = {
            "children": template_blocks
        }

        block_response = requests.patch(block_url, headers=headers, data=json.dumps(block_data))

def add_arxiv_to_notion(title, link):
    title_key = load_config().get('notion_title', "名前")
    link_key = load_config().get('notion_url', "URL")
    page_data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            f"{title_key}": {
                f"title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            f"{link_key}": {
                "url": link
            },
        }
    }
    add_to_notion(page_data)
