#!/usr/bin/env python3

# 必要なライブラリのインポート
import json
from datetime import datetime, timedelta
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys
import time
from dotenv import load_dotenv
load_dotenv('/app/.env')

# スクリプトのディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
# srcディレクトリをPythonパスに追加
sys.path.append(current_dir)


from utils import file_exists, save_to_json, load_from_json, load_config
from notion_api import get_notion_data, extract_notion_data, notion_url, headers, add_arxiv_to_notion
from openai_api import get_text_embedding, client, model
from arxiv_api import get_arxiv_paper_count, get_arxiv_papers, get_yesterdays_arxiv_paper_count, arxiv_link_to_id, get_arxiv_paper_info_by_id
from slack_api import post_to_slack, PAPER_NOTIFICATION_TEMPLETE

def arxiv2notion(paper_to_notion):
    """
    arxivから獲得したデータをnotion用のデータ構造に変換する
    """
    title = paper_to_notion["title"] + "(PaperPal)"
    link = paper_to_notion["link"]

    add_arxiv_to_notion(title, link)

def arxiv2slack(paper_to_slack, distance):
    title = paper_to_slack["title"].replace("\n", " ")
    summary = paper_to_slack["summary"].replace("\n", " ")
    link = paper_to_slack["link"]
    id = arxiv_link_to_id(link)
    message = PAPER_NOTIFICATION_TEMPLETE.format(title=title, summary=summary, distance=distance, id=id, link=link)
    slack_channel = load_config().get('slack_channel', None)
    post_to_slack(message, slack_channel)

def apply_function_to_links(data_list, function):
    results = []
    for item in data_list:
        if 'link' in item and item['link']:
            result = function(item['link'])
            results.append(result)
    return results

if __name__ == "__main__":
    # Notionデータからのデータ取得、knowledgeの更新、埋め込みベクトルの作成、保存、論文の推薦を行う
    test_mode = True
    if test_mode:
        post_to_slack(message="論文の探索中です", channel=load_config().get('slack_channel', None))

    knowledge_path = "/app/data/knowledge.json"

    # 既存のNotionからデータの取得
    """データ構造
    {"title": title, "link": link, "classification": classification}
    """

    # 適合するNotionデータベースを持っていない場合はinitial_data_pathとしてjsonファイルを渡すことも可能
    initial_data_path = load_config().get('initial_data_path', None)
    if file_exists(initial_data_path):
        """データ構造
        [{"title": title, "link": link}]
        """
        notion_data = load_from_json(initial_data_path)
        if load_config().get('add_to_notion', True):
            for idx in range(len(notion_data)):
                paper_to_notion = notion_data[idx]
                arxiv2notion(paper_to_notion)
    else:
        _notion_data = get_notion_data(notion_url, headers)
        notion_data = extract_notion_data(_notion_data)

    # NotionとKnowledgeの同期
    if file_exists(knowledge_path):
        # 既存のKnowledgeデータの取得
        """データ構造
        [{"text":{"title": title, "summary": summary}, "embedding":{"title": title, "summary": summary}, "id": id}]
        """
        knowledge_data = load_from_json(knowledge_path)
        # titleの突合とknowledgeへの追加
        count = 0
        for _notion_data in notion_data:
            if not any(_knowledge_data["text"]["title"] == _notion_data["title"] for _knowledge_data in knowledge_data):
                _title = _notion_data["title"]
                _id = arxiv_link_to_id(_notion_data["link"])
                count += 1
                print(f"Append {_title} into knowledge")
                if _id is None:
                    # arxivの論文ではなかった場合
                    knowledge_data.append( 
                        {
                            "text":{"title": _title, "summary": None}, 
                            "embedding":{"title": get_text_embedding(client, _title, model), "summary": get_text_embedding(client, _summary, model)}, 
                            "id": _id,
                        }
                    )
                else:
                    # arxivの論文だった場合
                    _summary = get_arxiv_paper_info_by_id(_id)[0]["summary"]

                    knowledge_data.append( 
                        {
                            "text":{"title": _title, "summary": _summary}, 
                            "embedding":{"title": get_text_embedding(client, _title, model), "summary": get_text_embedding(client, _summary, model)}, 
                            "id": _id,
                        }
                    )
        # Notionにないデータをknowledgeから削除する
        notion_titles = {entry['title'] for entry in notion_data}
        knowledge_data = [entry for entry in knowledge_data if entry["text"]['title'] in notion_titles]
        print(f"Appended {count} data into knowledge")
        save_to_json(knowledge_data, knowledge_path)
    else:
        # knowledgeからない場合の初期設定
        if test_mode:
            notion_data = notion_data[:10]
        knowledge_data = []
        count = 0
        for _notion_data in notion_data:
            _title = _notion_data["title"]
            _id = arxiv_link_to_id(_notion_data["link"])
            count += 1
            print(f"Append {_title} into knowledge")
            if _id is None:
                # arxivの論文ではなかった場合
                knowledge_data.append( 
                    {
                        "text":{"title": _title, "summary": None}, 
                        "embedding":{"title": get_text_embedding(client, _title, model), "summary": None}, 
                        "id": _id,
                    }
                )
            else:
                # arxivの論文だった場合
                _summary = get_arxiv_paper_info_by_id(_id)[0]["summary"]
                knowledge_data.append( 
                    {
                        "text":{"title": _title, "summary": _summary}, 
                        "embedding":{"title": get_text_embedding(client, _title, model), "summary": get_text_embedding(client, _summary, model)}, 
                        "id": _id,
                    }
                )
        print(f"Appended {count} data into knowledge")
        save_to_json(knowledge_data, knowledge_path)
    
    # Knowledgeに基づく論文の推薦

    # 前日に公開されたarxiv論文の取得
    yesterday = datetime.now() - timedelta(days=1)
    count = get_arxiv_paper_count(yesterday)
    print(f"Number of papers published yesterday: {count}")
    keywords = load_config().get('keywords', []) # フィルタリングに使用するキーワード
    filtered_papers = get_arxiv_papers(yesterday, keywords=keywords, max_result=count)
    if test_mode:
        filtered_papers = filtered_papers[:3]

    # 各論文のidの取得
    yesterday_arxiv_ids = apply_function_to_links(filtered_papers, arxiv_link_to_id)

    # 前日に公開されたarxiv論文の埋め込み表現化と登録
    arxiv_path = f"/app/data/embed_arxiv_{yesterday.year}-{yesterday.month}-{yesterday.day}.json"
    print(f"File {arxiv_path} does not exist. Creating new data...")
    arxiv_data = []
    for i, data in enumerate(filtered_papers):
        arxiv_data.append({
            "text":{"title": data['title'], "summary": data['summary']}, 
            "embedding":{"title": get_text_embedding(client, data["title"], model), "summary": get_text_embedding(client, data["title"], model)}, 
            "id": yesterday_arxiv_ids[i]
        })
    save_to_json(arxiv_data, arxiv_path)
    print(f"New data saved to {arxiv_path}")

    if count != 0:
        # 取得する論文の選定（top-N）
        # 既存データベースと新規取得データとの類似度獲得
        title_similarities = cosine_similarity(
            [item["embedding"]["title"] for item in arxiv_data],
            [item["embedding"]["title"] for item in knowledge_data]
            )
        title_distances = []
        for sim in title_similarities:
            title_distances.append(sum(sim) / len(sim))
        summary_similarities = cosine_similarity(
            [item["embedding"]["summary"] for item in arxiv_data],
            [item["embedding"]["summary"] for item in knowledge_data]
            )
        summary_distances = []
        for sim in summary_similarities:
            summary_distances.append(sum(sim) / len(sim))

        distances = [(x+y)/2 for x, y in zip(title_distances, summary_distances)]
        # 上位いくつの論文を取得するか
        sorted_indices = sorted(range(len(distances)), key=lambda i: distances[i], reverse=True)
        # Notionに論文を記録する
        if load_config().get('add_to_notion', True):
            for idx in sorted_indices[:load_config().get('arxiv_to_notion', 1)]:
                paper_to_notion = filtered_papers[idx]
                arxiv2notion(paper_to_notion)
        # Slackに論文を投稿する
        for idx in sorted_indices[:load_config().get('slack_to_notion', 3)]:
            paper_to_slack = filtered_papers[idx]
            arxiv2slack(paper_to_slack, distances[idx])
    else:
        """
        対象の日にarxivで公開された論文がなかったとき
        金曜日と土曜日、及び祝日には公開されない
        ref:https://info.arxiv.org/help/availability.html
        """
        post_to_slack(message="公開された論文はありません！", channel=load_config().get('slack_channel', None))
