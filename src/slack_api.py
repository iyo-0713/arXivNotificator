#!/usr/bin/env python3
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
load_dotenv('/app/.env')

PAPER_NOTIFICATION_TEMPLETE = """昨日公開された論文の中から、貴方の興味のあるものを選んできました！！
====================
ID: {id}
Title: {title}
Summary: {summary}
Link:{link}
興味度: {distance:.3f}
====================
"""

# slackへの投稿のテスト
def post_to_slack(message, channel='paper-notification'):
    client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    try:
        client.chat_postMessage(
            channel=channel,
            text=message
        )
    except SlackApiError as e:
        print(f"Error posting to Slack: {e.response['error']}")