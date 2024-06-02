#!/usr/bin/env python3
import feedparser
from datetime import datetime, timedelta
import re
import time

def get_arxiv_paper_count(date):
    time.sleep(3)
    base_url = f'http://export.arxiv.org/api/query?search_query=submittedDate:[{date.strftime("%Y%m%d")}0000+TO+{date.strftime("%Y%m%d")}2359]&start=0&max_results=0'
    feed = feedparser.parse(base_url)
    return int(feed.feed.opensearch_totalresults)

# 前日の論文の数を取得する
def get_yesterdays_arxiv_paper_count():
    yesterday = datetime.now() - timedelta(days=1)
    return get_arxiv_paper_count(yesterday)

def get_arxiv_papers(date, keywords=None, max_result=100):
    time.sleep(3)
    base_url = f'http://export.arxiv.org/api/query?search_query=submittedDate:[{date.strftime("%Y%m%d")}0000+TO+{date.strftime("%Y%m%d")}2359]&start=0&max_results={max_result}'
    feed = feedparser.parse(base_url)
    
    papers = []
    for entry in feed.entries:
        if keywords:
            if any(keyword.lower() in entry.title.lower() or keyword.lower() in entry.summary.lower() for keyword in keywords):
                paper = {
                    'title': entry.title.replace("\n", ", "),
                    'authors': [author.name for author in entry.authors],
                    'summary': entry.summary.replace("\n", ", "),
                    'published': entry.published,
                    'link': entry.link,
                    'pdf_link': entry.links[1].href
                }
                papers.append(paper)
        else:
            paper = {
                'title': entry.title.replace("\n", ", "),
                'authors': [author.name for author in entry.authors],
                'summary': entry.summary.replace("\n", ", "),
                'published': entry.published,
                'link': entry.link,
                'pdf_link': entry.links[1].href
            }
            papers.append(paper)
    
    return papers

# 前日の論文の数を取得する
def get_yesterdays_arxiv_papers(keywords=None, max_result=100):
    yesterday = datetime.now() - timedelta(days=1)
    return get_arxiv_papers(yesterday, keywords, max_result)

def arxiv_link_to_id(arxiv_link):
    if arxiv_link is None:
        return None
    """
    arxivのリンクからarxivのIDを取得する
    リンクがarxivのものでなければ None を返す
    """
    arxiv_patterns = [
        re.compile(r'arXiv\.(\d{4}\.\d{5})'), # (v\d+)?
        re.compile(r'arxiv.org/abs/(\d{4}\.\d{5})')
    ]
    for pattern in arxiv_patterns:
        match = pattern.search(arxiv_link)
        if match:
            arxiv_id = match.group(1) if match.group(1) else match.group(2)
            return arxiv_id
    return None

def get_arxiv_paper_info_by_id(arxiv_id):
    """
    arxivのidから論文の情報を取得する
    """
    time.sleep(3)
    base_url = 'http://export.arxiv.org/api/query?id_list='
    query_url = base_url + arxiv_id
    
    feed = feedparser.parse(query_url)
    
    papers = []
    for entry in feed.entries:
        try:
            published = entry.published
        except AttributeError as e:
            published = None
            print(f"#Error -> {e}")

        paper = {
            'title': entry.title.replace("\n", ", "),
            'authors': [author.name for author in entry.authors],
            'summary': entry.summary.replace("\n", ", "),
            'published': published,
            'link': entry.link,
            'pdf_link': entry.links[1].href if len(entry.links) > 1 else entry.link
        }
        papers.append(paper)
    
    return papers


