import argparse
import os
import json
from requests_html import HTMLSession
import operator
import requests
import time
import random

def get_media(user):
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    headers = {
        'User-Agent': 'My User Agent 1.0',
    }

    proxies = {
      'http': 'http://1.20.102.177:30106',
      'https': 'https://1.20.102.177:30106',
    }   
    url = 'https://www.instagram.com/' + user
    session = HTMLSession()
    req = session.get(url, headers=headers, proxies=proxies)
    
    media = []
    scripts = req.html.xpath('//script[@type]')    
    for s in scripts:
        content = s.text
        if "csrf_token" in content:
            content = content[:-1].split("window._sharedData = ")[1]      
            data = json.loads(content)     
            recent_media = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
            for r in recent_media:
                media.append({
                    "username": data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["username"],
                    "image": r["node"]["thumbnail_src"],
                    "timestamp": r["node"]["taken_at_timestamp"],
                    'permalink': r["node"]["display_url"],
                    'caption': r["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"],
                    'shortcode': r["node"]["shortcode"]
                })
    return media

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--users', '-u', nargs='+', help='Users to scrape images from')
    parser.add_argument('--output', '-o', help='Output file', required=True)
    args = parser.parse_args()
    assert args.users, "Enter users to scrape! Use --tags option, see help."
    all_media = []
    for user in args.users:
        all_media.extend(get_media(user))
        time.sleep(random.randint(1, 15))
    sorted_media = sorted(all_media, key=operator.itemgetter('timestamp'), reverse=True)
    sorted_media = sorted_media[:200]
    with open(args.output, 'w') as f:
        f.write(json.dumps(all_media))


