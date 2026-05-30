from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from models.item import Item


URL = "https://www.4gamer.net/indextop/all_interview_1.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


DATE_FORMATS = [
    "%Y/%m/%d %H:%M",
    "%Y/%m/%d",
]


def parse_date(text: str) -> datetime | None:

    text = text.strip()

    for fmt in DATE_FORMATS:

        try:
            return datetime.strptime(
                text,
                fmt
            )

        except ValueError:
            pass

    return None


def parse():

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    response.encoding = (
        response.apparent_encoding
        or "euc_jp"
    )

    soup = BeautifulSoup(
        response.text,
        "lxml"
    )

    articles = soup.select(
        'div[class*="V2_article_container"]'
    )

    items = []

    for article in articles:

        try:

            title_el = article.select_one(
                "h2 a"
            )

            if not title_el:
                continue

            desc_el = article.select_one(
                'p[class*="lead_container"]'
            )

            date_el = article.select_one(
                ".timestamp"
            )

            img_el = article.select_one(
                'img[class*="img_right_top"]'
            )

            title = title_el.get_text(
                strip=True
            )

            link = urljoin(
                "https://www.4gamer.net",
                title_el.get("href", "")
            )

            description = ""

            if desc_el:
                description = desc_el.get_text(
                    " ",
                    strip=True
                )

            if not description:
                description = title

            pub_date = None
            if date_el:

                raw_date = date_el.get_text(
                    " ",
                    strip=True
                )

                pub_date = parse_date(
                    raw_date
                )

                if pub_date is None:

                    print(
                        "[4Gamer] Date parse failed:",
                        repr(raw_date)
                    )

            image_url = ""

            if img_el:

                image_url = (
                    img_el.get("src")
                    or img_el.get("data-src")
                    or ""
                )

                image_url = urljoin(
                    "https://www.4gamer.net",
                    image_url
                )

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

            print(
                f"[4Gamer] Parse error: {e}"
            )

    return items
