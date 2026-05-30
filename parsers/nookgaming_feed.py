import re

import requests

from bs4 import BeautifulSoup
from datetime import datetime

from models.item import Item


URL = "https://game.watch.impress.co.jp/docs/interview/"

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
        "section.list ul.list-02 li.item.interview"
    )

    for article in articles:

        try:

            title_el = article.select_one(
                'p[class*="title"]'
            )

            link_el = article.select_one(
                'p[class*="title"] a'
            )

            if not title_el or not link_el:
                continue

            title = title_el.get_text(
                " ",
                strip=True
            )

            link = (
                link_el.get("href", "")
                .strip()
            )

            if link.startswith("/"):
                link = (
                    "https://game.watch.impress.co.jp"
                    + link
                )

            desc_el = article.select_one(
                'p[class*="outline"]'
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
                'div[class*="image"] img'
            )

            if img_el:

                image_url = (
                    img_el.get("src")
                    or img_el.get("data-src")
                    or ""
                )

                if image_url.startswith("/"):
                    image_url = (
                        "https://game.watch.impress.co.jp"
                        + image_url
                    )

            pub_date = None

            date_el = article.select_one(
                'p[class*="date"]'
            )

            if date_el:

                raw_date = date_el.get_text(
                    strip=True
                )

                match = re.search(
                    r"\((\d{4})/(\d{1,2})/(\d{1,2})\)",
                    raw_date
                )

                if match:

                    pub_date = datetime(
                        int(match.group(1)),
                        int(match.group(2)),
                        int(match.group(3))
                    )

            items.append(
                Item(
                    site="GameWatch",
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
                f"[GameWatch] {e}"
            )

    return items
