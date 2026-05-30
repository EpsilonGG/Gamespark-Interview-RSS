from datetime import datetime

import feedparser

from bs4 import BeautifulSoup

from models.item import Item


FEED_URL = "https://www.nookgaming.com/feed/"


def clean_html(html: str) -> str:

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    return soup.get_text(
        " ",
        strip=True
    )


def parse():

    feed = feedparser.parse(
        FEED_URL
    )

    items = []

    for entry in feed.entries:

        try:

            title = (
                entry.get(
                    "title",
                    ""
                )
                .strip()
            )

            link = (
                entry.get(
                    "link",
                    ""
                )
                .strip()
            )

            description = ""

            if entry.get("summary"):

                description = clean_html(
                    entry.summary
                )

            pub_date = None

            if entry.get(
                "published_parsed"
            ):

                pub_date = datetime(
                    *entry.published_parsed[:6]
                )

            image_url = ""

            if entry.get(
                "media_content"
            ):

                media = (
                    entry.media_content
                )

                if (
                    media
                    and media[0].get("url")
                ):

                    image_url = (
                        media[0]["url"]
                    )

            elif entry.get(
                "media_thumbnail"
            ):

                media = (
                    entry.media_thumbnail
                )

                if (
                    media
                    and media[0].get("url")
                ):

                    image_url = (
                        media[0]["url"]
                    )

            items.append(
                Item(
                    site="NookGaming",
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
                f"[NookGaming] {e}"
            )

    return items
