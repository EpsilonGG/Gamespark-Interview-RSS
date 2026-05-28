```python id="g4vjv0"
import requests
from bs4 import BeautifulSoup
from datetime import datetime


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

    items = soup.select("section.item")

    results = []

    for item in items[:10]:

        try:

            # 标题
            title_el = item.select_one(".title")

            # 摘要
            summary_el = item.select_one(".summary")

            # 链接
            link_el = item.select_one("a.link")

            # 时间
            date_el = item.select_one("time.date")

            # 图片
            img_el = item.select_one("img.figure")

            if not title_el or not link_el:
                continue

            title = title_el.get_text(strip=True)

            link = link_el.get("href", "")

            # 补全相对链接
            if link.startswith("/"):
                link = "https://www.gamespark.jp" + link

            # 摘要
            description = ""

            if summary_el:
                description = summary_el.get_text(strip=True)

            # 发布时间
            pub_date = None

            if date_el:

                raw_date = date_el.get_text(strip=True)

                try:
                    pub_date = datetime.strptime(
                        raw_date,
                        "%Y.%m.%d %a %H:%M"
                    )

                except Exception:
                    pass

            # 图片
            image_url = ""

            if img_el:

                image_url = img_el.get("src", "")

                # lazyload兼容
                if not image_url:
                    image_url = img_el.get("data-src", "")

                # 补全相对路径
                if image_url.startswith("/"):
                    image_url = "https://www.gamespark.jp" + image_url

            # 保存结果
            results.append({

                "site": "gamespark",

                "title": title,

                "link": link,

                "description": description,

                "pub_date": pub_date,

                "image_url": image_url,
            })

        except Exception as e:

            print("Game*Spark parse error:", e)

    return results
```
