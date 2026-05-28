from dataclasses import dataclass
from datetime import datetime


@dataclass
class Item:
    site: str
    category: str
    title: str
    link: str
    description: str
    image_url: str
    pub_date: datetime | None
    tags: list[str]
