#!/usr/bin/env python3
import os
from openai import OpenAI
import openai
from dotenv import load_dotenv
load_dotenv('/app/.env')

# OpenAIに関する設定
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()
model = "text-embedding-3-small" # "text-embedding-3-large", "ada v2"


def get_text_embedding(client, text, model):
    """
    テキストの埋め込みベクトルを取得する。
    """
    if text == None:
        return None
    try:
        response = client.embeddings.create(model=model, input=text, encoding_format="float")
        return response.data[0].embedding
    except Exception as e:
        print(f"An error occurred: {e}")
        return None