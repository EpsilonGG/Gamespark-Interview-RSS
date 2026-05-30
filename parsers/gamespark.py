import requests

from bs4 import BeautifulSoup
from datetime import datetime

from models.item import Item


URL = (
    "https://www.gamespark.jp/"
    "category/featured/interview/latest/"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def parse():

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "lxml"
    )

    items = []

    articles = soup.select(
        "section.item"
    )

    for article in articles:

        try:

            title_el = article.select_one(
                ".title"
            )

            link_el = article.select_one(
                "a.link"
            )

            if not title_el or not link_el:
                continue

            title = title_el.get_text(
                strip=True
            )

            link = (
                link_el.get("href", "")
                .strip()
            )

            if link.startswith("/"):

                link = (
                    "https://www.gamespark.jp"
                    + link
                )

            desc_el = article.select_one(
                ".summary"
            )

            description = (
                desc_el.get_text(
                    " ",
                    strip=True
                )
                if desc_el
                else ""
            )

            image_url = ""

            img_el = article.select_one(
                "img.figure"
            )

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

            pub_date = None

            date_el = article.select_one(
                "time.date"
            )

            if date_el:

                raw_date = (
                    date_el.get("datetime")
                    or date_el.get_text(
                        strip=True
                    )
                )

                try:

                    dt = datetime.fromisoformat(
                        raw_date.replace(
                            "Z",
                            "+00:00"
                        )
                    )

                    # 统一转 naive datetime
                    pub_date = dt.replace(
                        tzinfo=None
                    )

                except Exception:

                    try:

                        pub_date = datetime.strptime(
                            raw_date,
                            "%Y.%m.%d %a %H:%M"
                        )

                    except Exception:

                        pub_date = None

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

            print(
                f"[Game*Spark] {e}"
            )

    return items
