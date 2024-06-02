#!/usr/bin/env python3
import os
import json

def file_exists(file_path):
    """
    ファイルの存在を確認する。
    """
    return os.path.exists(file_path)

def save_to_json(data, file_path):
    """
    データをJSONファイルに保存する。
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json(file_path):
    """
    JSONファイルからデータを読み込む。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def load_config():
    """
    configの情報を取得する
    key = "keywords", "slack_channel"
    """
    with open('/app/config.json', 'r') as f:
        config = json.load(f)
    return config