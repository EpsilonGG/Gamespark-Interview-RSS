import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re


URL = "https://www.famitsu.com/category/interview/page/1"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def parse_famitsu():

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    items = soup.select(
        "div[class*='PrimaryCard_cardContainer'], "
        "div[class*='SecondaryCard_card']"
    )

    results = []

    for item in items[:10]:

        try:

            # 标题
            title_el = item.select_one('a[class*="title"]')

            # 摘要
            desc_el = item.select_one('a[class*="lead"]')

            # 时间
            date_el = item.select_one('div[class*="date"] time')

            # 图片
            img_el = item.select_one('div[class*="media"] img')

            if not title_el:
                continue

            # 标题
            title = title_el.get_text(strip=True)

            # 链接
            link = title_el.get("href", "")

            # 补全相对链接
            if link.startswith("/"):
                link = "https://www.famitsu.com" + link

            # 摘要
            description = ""

            if desc_el:
                description = desc_el.get_text(strip=True)

            # 发布时间
            pub_date = None

            if date_el:

                raw_date = date_el.get_text(strip=True)

                # 处理 "3日前"
                match = re.search(r"(\d+)日前", raw_date)

                if match:

                    days_ago = int(match.group(1))

                    pub_date = datetime.now() - timedelta(days=days_ago)

                else:
                    pub_date = datetime.now()

            # 图片
            image_url = ""

            if img_el:

                image_url = img_el.get("src", "")

                # lazyload兼容
                if not image_url:
                    image_url = img_el.get("data-src", "")

                # 补全相对路径
                if image_url.startswith("/"):
                    image_url = "https://www.famitsu.com" + image_url

            # 保存结果
            results.append({

                "site": "famitsu",

                "title": title,

                "link": link,

                "description": description,

                "pub_date": pub_date,

                "image_url": image_url,
            })

        except Exception as e:

            print("Famitsu parse error:", e)

    return results
