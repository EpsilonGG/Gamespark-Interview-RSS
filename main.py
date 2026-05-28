import json

from datetime import datetime, timezone

from feedgen.feed import FeedGenerator

from parsers.gamespark import parse_gamespark
from parsers.fourgamer import parse_fourgamer
from parsers.famitsu import parse_famitsu
from parsers.gamewatch import parse_gamewatch
from parsers.nookgaming_feed import parse_nookgaming_feed

from utils.dedup import remove_duplicates


# =========================
# 统一 datetime
# =========================

def normalize_pub_date(dt):

    if dt is None:
        return None

    # naive datetime -> UTC
    if dt.tzinfo is None:

        dt = dt.replace(
            tzinfo=timezone.utc
        )

    # aware datetime -> 转 UTC
    else:

        dt = dt.astimezone(
            timezone.utc
        )

    return dt


# =========================
# history 文件
# =========================

HISTORY_FILE = "storage/history.json"


# =========================
# 读取 history
# =========================

try:

    with open(
        HISTORY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        history = json.load(f)

except:

    history = []


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
# 去重
# =========================

all_items = remove_duplicates(all_items)


# =========================
# 统一 pub_date
# =========================

for item in all_items:

    item.pub_date = normalize_pub_date(
        item.pub_date
    )


# =========================
# 按时间排序
# =========================

all_items.sort(
    key=lambda x: (
        x.pub_date
        or datetime.min.replace(
            tzinfo=timezone.utc
        )
    ),
    reverse=True
)


# =========================
# 找出新增内容
# =========================

new_items = []

for item in all_items:

    if item.link not in history:

        new_items.append(item)


# =========================
# 保存完整新增列表
# （用于 history）
# =========================

all_new_items = new_items.copy()


# =========================
# RSS 输出数量限制
# =========================

MAX_ITEMS = 50

new_items = new_items[:MAX_ITEMS]


# =========================
# 创建 RSS
# =========================

fg = FeedGenerator()

fg.title("Japanese Game Media RSS")

fg.link(
    href="https://www.gamespark.jp/"
)

fg.description(
    "Japanese game interview / review aggregation"
)

fg.language("ja")


# =========================
# 添加 RSS Item
# =========================

for item in new_items:

    fe = fg.add_entry()

    # 标题
    fe.title(
        f"[{item.site}] {item.title}"
    )

    # 链接
    fe.link(
        href=item.link
    )

    # guid
    fe.guid(item.link)

    # 发布时间
    if item.pub_date:

        fe.pubDate(
            item.pub_date
        )

    # description
    description_html = ""

    if item.image_url:

        description_html += (
            f'<img src="{item.image_url}"><br>'
        )

    if item.description:

        description_html += (
            item.description
        )

    fe.description(
        description_html
    )

    # enclosure
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


# =========================
# 更新 history
# （注意：保存全部新增）
# =========================

for item in all_new_items:

    history.append(
        item.link
    )


# =========================
# 保存 history
# =========================

with open(
    HISTORY_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        history,
        f,
        ensure_ascii=False,
        indent=2
    )


# =========================
# 输出日志
# =========================

print(
    "RSS generated successfully!"
)

print(
    f"Total items fetched: {len(all_items)}"
)

print(
    f"New items found: {len(all_new_items)}"
)

print(
    f"RSS items output: {len(new_items)}"
)
