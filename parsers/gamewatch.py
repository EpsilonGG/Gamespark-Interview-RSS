import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from models.item import Item

URL = "https://game.watch.impress.co.jp/docs/interview/"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def parse_gamewatch():

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    items = soup.select(
        "section.list ul.list-02 li.item.interview"
    )

    results = []

    for item in items[:10]:

        try:

            # 标题
            title_el = item.select_one('p[class*="title"]')

            # 摘要
            desc_el = item.select_one('p[class*="outline"]')

            # 链接
            link_el = item.select_one('p[class*="title"] a')

            # 时间
            date_el = item.select_one('p[class*="date"]')

            # 图片
            img_el = item.select_one('div[class*="image"] a img')

            if not title_el or not link_el:
                continue

            # 标题
            title = title_el.get_text(strip=True)

            # 链接
            link = link_el.get("href", "")

            # 补全相对路径
            if link.startswith("/"):
                link = "https://game.watch.impress.co.jp" + link

            # 摘要
            description = ""

            if desc_el:
                description = desc_el.get_text(strip=True)

            # 发布时间
            pub_date = None

            if date_el:

                raw_date = date_el.get_text(strip=True)

                # 提取 (2026/5/28)
                match = re.search(
                    r"\((\d{4})/(\d{1,2})/(\d{1,2})\)",
                    raw_date
                )

                if match:

                    year = int(match.group(1))
                    month = int(match.group(2))
                    day = int(match.group(3))

                    pub_date = datetime(
                        year,
                        month,
                        day
                    )

            # 图片
            image_url = ""

            if img_el:

                image_url = img_el.get("src", "")

                # lazyload兼容
                if not image_url:
                    image_url = img_el.get("data-src", "")

                # 补全相对路径
                if image_url.startswith("/"):
                    image_url = (
                        "https://game.watch.impress.co.jp"
                        + image_url
                    )

            # 保存结果
            results.append({

                "site": "gamewatch",

                "title": title,

                "link": link,

                "description": description,

                "pub_date": pub_date,

                "image_url": image_url,
            })

        except Exception as e:

            print("Game Watch parse error:", e)

    return results
