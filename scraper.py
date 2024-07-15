import json
import requests
from bs4 import BeautifulSoup

def load_cookies(cookie_file):
    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
    return cookies

def fetch_xiaohongshu_post_data(url, cookies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取数据
    title = soup.find('meta', {'name': 'og:title'}).get('content', 'N/A')
    likes = soup.find('meta', {'name': 'og:xhs:note_like'}).get('content', 'N/A')
    favorites = soup.find('meta', {'name': 'og:xhs:note_collect'}).get('content', 'N/A')
    comments = soup.find('meta', {'name': 'og:xhs:note_comment'}).get('content', 'N/A')

    return {
        'title': title,
        'likes': likes,
        'favorites': favorites,
        'comments': comments,
        'shares': 'N/A'  # Assuming there's no meta tag for shares
    }
