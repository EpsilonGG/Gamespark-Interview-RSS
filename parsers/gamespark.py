import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models.item import Item


URL = "https://www.gamespark.jp/category/featured/interview/latest/"


headers = {
    "User-Agent": "Mozilla/5.0"
}


def parse_gamespark():

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    articles = soup.select("section.item")

    items = []

    for article in articles[:20]:

        try:

            # 标题
            title_el = article.select_one(".title")

            # 摘要
            desc_el = article.select_one(".summary")

            # 链接
            link_el = article.select_one("a.link")

            # 日期
            date_el = article.select_one("time.date")

            # 图片
            img_el = article.select_one("img.figure")

            if not title_el or not link_el:
                continue

            # 标题
            title = title_el.get_text(strip=True)

            # 链接
            link = link_el.get("href", "").strip()

            if link.startswith("/"):
                link = "https://www.gamespark.jp" + link

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

                raw_date = (
                    date_el.get("datetime")
                    or date_el.get_text(strip=True)
                )

                try:
                    pub_date = datetime.fromisoformat(
                        raw_date.replace("Z", "+00:00")
                    )

                except:

                    try:
                        pub_date = datetime.strptime(
                            raw_date,
                            "%Y.%m.%d %a %H:%M"
                        )

                    except:
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
                        "https://www.gamespark.jp"
                        + image_url
                    )

            # 保存 Item
            items.append(
                Item(
                    site="Game*Spark",
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

            print("[Game*Spark] Parse Error:", e)

    return items
