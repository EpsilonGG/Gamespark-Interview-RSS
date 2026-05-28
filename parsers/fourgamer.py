import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models.item import Item


URL = "https://www.4gamer.net/indextop/all_interview_1.html"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def parse_fourgamer():

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    articles = soup.select(
        'div[class*="V2_article_container"]'
    )

    items = []

    for article in articles:

        try:

            # 标题
            title_el = article.select_one("h2 a")

            # 摘要
            desc_el = article.select_one(
                'p[class*="lead_container"]'
            )

            # 时间
            date_el = article.select_one(".timestamp")

            # 图片
            img_el = article.select_one(
                'img[class*="img_right_top"]'
            )

            if not title_el:
                continue

            # 标题
            title = title_el.get_text(strip=True)

            # 链接
            link = title_el.get("href", "").strip()

            if link.startswith("/"):
                link = "https://www.4gamer.net" + link

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

                raw_date = date_el.get_text(strip=True)

                try:
                    pub_date = datetime.strptime(
                        raw_date,
                        "%Y/%m/%d %H:%M"
                    )

                except Exception:
                    pub_date = None

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
                        "https://www.4gamer.net"
                        + image_url
                    )

            # 保存 Item
            items.append(
                Item(
                    site="4Gamer",
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

            print(f"[4Gamer] Error: {e}")

    return items
