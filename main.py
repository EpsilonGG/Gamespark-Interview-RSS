from datetime import datetime, timezone
from feedgen.feed import FeedGenerator

from parsers.gamespark import parse_gamespark
from parsers.fourgamer import parse_fourgamer
from parsers.famitsu import parse_famitsu
from parsers.gamewatch import parse_gamewatch
from parsers.nookgaming_feed import parse_nookgaming_feed


# =========================
# 统一 datetime
# aware -> UTC naive
# =========================

def normalize_pub_date(dt):

    if dt is None:
        return None

    # aware datetime
    if dt.tzinfo is not None:

        dt = (
            dt.astimezone(timezone.utc)
            .replace(tzinfo=None)
        )

    return dt


# =========================
# 收集所有站点内容
# =========================

all_items = []

try:
    all_items.extend(parse_gamespark())
except Exception as e:
    print("[GameSpark] Error:", e)

try:
    all_items.extend(parse_fourgamer())
except Exception as e:
    print("[4Gamer] Error:", e)

try:
    all_items.extend(parse_famitsu())
except Exception as e:
    print("[Famitsu] Error:", e)

try:
    all_items.extend(parse_gamewatch())
except Exception as e:
    print("[GameWatch] Error:", e)

try:
    all_items.extend(parse_nookgaming_feed())
except Exception as e:
    print("[NookGaming] Error:", e)


# =========================
# 统一所有 pub_date
# =========================

for item in all_items:

    item.pub_date = normalize_pub_date(
        item.pub_date
    )


# =========================
# 按发布时间排序
# =========================

all_items.sort(
    key=lambda x: x.pub_date or datetime.min,
    reverse=True
)


# =========================
# RSS总条数限制
# =========================

MAX_ITEMS = 50

all_items = all_items[:MAX_ITEMS]


# =========================
# 创建 RSS
# =========================

fg = FeedGenerator()

fg.title("Japanese Game Media RSS")
fg.link(href="https://www.gamespark.jp/")
fg.description(
    "Japanese game interview / review aggregation"
)
fg.language("ja")


# =========================
# 添加 RSS Item
# =========================

for item in all_items:

    fe = fg.add_entry()

    # 标题
    fe.title(f"[{item.site}] {item.title}")

    # 链接
    fe.link(href=item.link)

    # guid
    fe.guid(item.link)

    # 发布时间
    if item.pub_date:
        fe.pubDate(item.pub_date)

    # description
    description_html = ""

    if item.image_url:
        description_html += (
            f'<img src="{item.image_url}"><br>'
        )

    if item.description:
        description_html += item.description

    fe.description(description_html)

    # enclosure（部分 RSS 阅读器显示缩略图）
    if item.image_url:
        fe.enclosure(
            item.image_url,
            0,
            "image/jpeg"
        )


# =========================
# 输出 rss.xml
# =========================

fg.rss_file("rss.xml")

print("RSS generated successfully!")
print(f"Total items: {len(all_items)}")
