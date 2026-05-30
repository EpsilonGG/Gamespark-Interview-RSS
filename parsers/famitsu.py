import re
from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from models.item import Item


URL = "https://www.famitsu.com/category/interview/page/1"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}


def parse_relative_date(text: str) -> datetime | None:

    text = text.strip()

    now = datetime.now()

    if text == "昨日":
        return now - timedelta(days=1)

    if text == "一昨日":
        return now - timedelta(days=2)

    patterns = [
        (r"(\d+)分前", "minutes"),
        (r"(\d+)時間前", "hours"),
        (r"(\d+)日前", "days"),
        (r"(\d+)週間前", "weeks"),
        (r"(\d+)(?:か月|ヶ月)前", "months"),
        (r"(\d+)年前", "years"),
    ]

    for pattern, unit in patterns:

        match = re.search(pattern, text)

        if not match:
            continue

        value = int(match.group(1))

        if unit == "minutes":
            return now - timedelta(minutes=value)

        if unit == "hours":
            return now - timedelta(hours=value)

        if unit == "days":
            return now - timedelta(days=value)

        if unit == "weeks":
            return now - timedelta(weeks=value)

        if unit == "months":
            return now - timedelta(days=value * 30)

        if unit == "years":
            return now - timedelta(days=value * 365)

    return None


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

    articles = soup.select(
        "div[class*='PrimaryCard_cardContainer'], "
        "div[class*='SecondaryCard_card']"
    )

    items = []

    for article in articles:

        try:

            title_el = article.select_one(
                'a[class*="title"]'
            )

            if not title_el:
                continue

            desc_el = article.select_one(
                'a[class*="lead"]'
            )

            date_el = article.select_one(
                'div[class*="date"] time'
            )

            img_el = article.select_one(
                'div[class*="media"] img'
            )

            title = title_el.get_text(
                strip=True
            )

            link = urljoin(
                "https://www.famitsu.com",
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
                    strip=True
                )

                pub_date = parse_relative_date(
                    raw_date
                )

            image_url = ""

            if img_el:

                image_url = (
                    img_el.get("src")
                    or img_el.get("data-src")
                    or img_el.get("data-original")
                    or ""
                )

                image_url = urljoin(
                    "https://www.famitsu.com",
                    image_url
                )

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
