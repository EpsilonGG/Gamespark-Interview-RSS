import requests
from bs4 import BeautifulSoup
from datetime import datetime


URL = "https://www.nookgaming.com/"


def parse_nookgaming():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    items = []

    articles = soup.select(
        'div[class*="fp-col"][class*="fp-post"]'
    )

    for article in articles:
        try:
            title_el = article.select_one(".fp-title a")
            desc_el = article.select_one(".fp-excerpt")
            date_el = article.select_one(".fp-date time")
            img_el = article.select_one(".fp-thumbnail img")

            if not title_el:
                continue

            title = title_el.get_text(strip=True)

            link = title_el.get("href", "").strip()

            if link.startswith("/"):
                link = "https://www.nookgaming.com" + link

            description = ""
            if desc_el:
                description = desc_el.get_text(" ", strip=True)

            image_url = ""
            if img_el:
                image_url = (
                    img_el.get("src")
                    or img_el.get("data-src")
                    or ""
                )

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
                    pub_date = None

            items.append({
                "site": "NookGaming",
                "category": "review",
                "title": title,
                "link": link,
                "description": description,
                "image_url": image_url,
                "pub_date": pub_date,
                "tags": []
            })

        except Exception as e:
            print(f"[NookGaming] Error: {e}")

    return items
