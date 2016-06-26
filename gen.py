import requests
import json
import time
from operator import itemgetter
from jinja2 import Template
from bs4 import BeautifulSoup

def read_file(file):
    with open(file, 'r') as content_file:
        content = content_file.read()
    return content

def create_file(file_name, file_content):
    f = open(file_name, 'wb')
    f.write(file_content)
    f.close()

users = ["pdpatt", "demar_derozan", "kyle_lowry7", "jvalanciunas", "3tross1", "lucasbebenogueira", "brunofive", "demarrecarroll1", "coryjoseph", "dwfivefive", "normanpowell4", "pskills43", "bismackbiyombo", "iamjames_johnson3"]

all_media = []
for u in users:
    try:
      soup = BeautifulSoup(requests.get("http://www.instagram.com/" + u).text, "html.parser")
      scripts = soup.find_all("script")
      data = json.loads(scripts[6].get_text()[:-1].split("window._sharedData = ")[1])
      recent_media = data["entry_data"]["ProfilePage"][0]["user"]["media"]["nodes"]
      for r in recent_media:
          r["user"] = data["entry_data"]["ProfilePage"][0]["user"]
          r['time'] = time.strftime('%b %d, %Y', time.localtime(r['date']))
      all_media.extend(recent_media)
    except Exception, e:
      print e
      continue
sorted_media = sorted(all_media, key=itemgetter('date'), reverse=True)
sorted_media = sorted_media[:200]
info = {'bits': sorted_media}
template = Template(read_file('./insta.html'))
print template.render(info).encode("utf-8")
