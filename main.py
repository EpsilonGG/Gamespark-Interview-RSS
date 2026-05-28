from email.utils import format_datetime
from datetime import datetime
from feedgen.feed import FeedGenerator
from email.utils import format_datetime

# 导入 parser
from parsers.gamespark import parse_gamespark
from parsers.fourgamer import parse_fourgamer
from parsers.famitsu import parse_famitsu
from parsers.gamewatch import parse_gamewatch
from parsers.nookgaming_feed import parse_nookgaming_feed

# =========================
# 创建 RSS Feed
# =========================

fg = FeedGenerator()

fg.title("Japanese Game Interview RSS")
fg.link(href="https://www.gamespark.jp/")
fg.description("Game interview aggregation feed")
fg.language("ja")


# =========================
# 收集所有网站数据
# =========================

all_items = []

# Game*Spark
all_items.extend(parse_gamespark())

# 4Gamer
all_items.extend(parse_fourgamer())

# Famitsu 
all_items.extend(parse_famitsu())

# Game Watch 
all_items.extend(parse_gamewatch())

# NookGaming
all_items.extend(parse_nookgaming_feed())

# =========================
# 按发布时间排序（新→旧）
# =========================

all_items.sort(
    key=lambda x: x.get("pub_date") or datetime.min,
    reverse=True
)


# =========================
# 限制 RSS 条数
# =========================

MAX_ITEMS = 10

all_items = all_items[:MAX_ITEMS]


# =========================
# 生成 RSS Item
# =========================

for item in all_items:

    fe = fg.add_entry()

    # 标题
    site_name = item.get("site", "").upper()
    rss_title = f"[{site_name}] {item['title']}"
    fe.title(rss_title)

    # 链接
    fe.link(href=item["link"])

    # GUID（防止重复推送）
    fe.guid(item["link"], permalink=True)

    # description
    # Telegram 推荐留空
    fe.description("")

    # 发布时间
    if item.get("pub_date"):
        fe.pubDate(
            format_datetime(item["pub_date"])
        )

    # 图片（TG / Feedly 可识别）
    if item.get("image_url"):

        fe.enclosure(
            item["image_url"],
            0,
            "image/jpeg"
        )


# =========================
# 输出 rss.xml
# =========================

rss_data = fg.rss_str(pretty=True)

with open("rss.xml", "wb") as f:
    f.write(rss_data)

print("rss.xml generated successfully")
