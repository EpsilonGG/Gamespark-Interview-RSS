import feedparser
from bs4 import BeautifulSoup
from datetime import datetime


FEED_URL = "https://www.nookgaming.com/feed/"


def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(" ", strip=True)


def parse_nookgaming_feed():
    feed = feedparser.parse(FEED_URL)

    items = []

    for entry in feed.entries:
        try:
            title = entry.get("title", "").strip()

            link = entry.get("link", "").strip()

            description = ""

            if "summary" in entry:
                description = clean_html(entry.summary)

                # 裁剪长度
                description = description[:200]

            pub_date = None

            if "published_parsed" in entry:
                pub_date = datetime(*entry.published_parsed[:6])

            image_url = ""

            # WordPress media content
            if "media_content" in entry:
                media = entry.media_content

                if media and "url" in media[0]:
                    image_url = media[0]["url"]

            items.append({
                "site": "NookGaming",
                "category": "review",
                "title": title,
                "link": link,
                "description": description,
                "image_url": image_url,
                "pub_date": pub_date,
                "tags": []
            })

        except Exception as e:
            print(f"[NookGaming Feed] Error: {e}")

    return items
