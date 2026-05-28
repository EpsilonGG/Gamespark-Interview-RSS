import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
from email.utils import format_datetime

URL = "https://www.gamespark.jp/category/featured/interview/latest/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

items = soup.select("section.item")

fg = FeedGenerator()

fg.title("Game*Spark Interview RSS")
fg.link(href=URL)
fg.description("Latest interviews from Game*Spark")
fg.language("ja")

for item in items[:20]:

    title_el = item.select_one(".title")
    link_el = item.select_one("a.link")
    summary_el = item.select_one(".summary")
    date_el = item.select_one("time.date")

    if not title_el or not link_el:
        continue

    title = title_el.get_text(strip=True)

    link = link_el.get("href", "")

    if link.startswith("/"):
        link = "https://www.gamespark.jp" + link

    summary = ""
    if summary_el:
        summary = summary_el.get_text(strip=True)

    pub_date = None

    if date_el:
        raw_date = date_el.get_text(strip=True)

        try:
            # 示例：
            # 2026.5.28 Thu 10:00
            pub_date = datetime.strptime(
                raw_date,
                "%Y.%m.%d %a %H:%M"
            )
        except:
            pass

    fe = fg.add_entry()

    fe.title(title)
    fe.link(href=link)
    fe.description(summary)
    fe.guid(link, permalink=True)

    if pub_date:
        fe.pubDate(format_datetime(pub_date))

rss_data = fg.rss_str(pretty=True)

with open("rss.xml", "wb") as f:
    f.write(rss_data)

print("rss.xml generated successfully")