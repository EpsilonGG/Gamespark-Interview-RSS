import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

from models.item import Item


URL = "https://www.famitsu.com/category/interview/page/1"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}


def parse_relative_date(text):

    text = text.strip()

    # 例：3日前
    match = re.search(r"(\d+)日前", text)

    if match:
        days = int(match.group(1))
        return datetime.now() - timedelta(days=days)

    # 例：5時間前
    match = re.search(r"(\d+)時間前", text)

    if match:
        hours = int(match.group(1))
        return datetime.now() - timedelta(hours=hours)

    # 例：20分前
    match = re.search(r"(\d+)分前", text)

    if match:
        minutes = int(match.group(1))
        return datetime.now() - timedelta(minutes=minutes)

    return None


def parse_famitsu():

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    articles = soup.select(
        "div[class*='PrimaryCard_cardContainer'], "
        "div[class*='SecondaryCard_card']"
    )

    items = []

    for article in articles:

        try:

            # 标题
            title_el = article.select_one(
                'a[class*="title"]'
            )

            # 摘要
            desc_el = article.select_one(
                'a[class*="lead"]'
            )

            # 时间
            date_el = article.select_one(
                'div[class*="date"] time'
            )

            # 图片
            img_el = article.select_one(
                'div[class*="media"] img'
            )

            if not title_el:
                continue

            # 标题
            title = title_el.get_text(strip=True)

            # 链接
            link = title_el.get("href", "").strip()

            if link.startswith("/"):
                link = "https://www.famitsu.com" + link

            # 摘要
            description = ""

            if desc_el:
                description = desc_el.get_text(
                    " ",
                    strip=True
                )

            # 发布时间
            pub_date = None

            if date_el:

                raw_date = date_el.get_text(
                    strip=True
                )

                pub_date = parse_relative_date(
                    raw_date
                )

            # 图片
            image_url = ""

            if img_el:

                image_url = (
                    img_el.get("src")
                    or img_el.get("data-src")
                    or ""
                )

                if image_url.startswith("/"):
                    image_url = (
                        "https://www.famitsu.com"
                        + image_url
                    )

            # 保存 Item
            items.append(
                Item(
                    site="Famitsu",
                    category="interview",
                    title=title,
                    link=link,
                    description=description,
                    image_url=image_url,
                    pub_date=pub_date,
                    tags=[]
                )
            )

        except Exception as e:

            print(
                f"[Famitsu] Parse error: {e}"
            )

    return items
