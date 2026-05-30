import json
import pkgutil
import importlib

from datetime import datetime, timezone
from feedgen.feed import FeedGenerator


HISTORY_FILE = "storage/history.json"


# =====================
# 自动发现 Parser
# =====================

def load_all_items():

    items = []

    import parsers

    for module_info in pkgutil.iter_modules(
        parsers.__path__
    ):

        module_name = module_info.name

        try:

            module = importlib.import_module(
                f"parsers.{module_name}"
            )

            if not hasattr(module, "parse"):
                continue

            result = module.parse()

            if result:
                items.extend(result)

            print(
                f"[OK] {module_name}: "
                f"{len(result)} items"
            )

        except Exception as e:

            print(
                f"[ERROR] {module_name}: {e}"
            )

    return items


# =====================
# history
# =====================

try:

    with open(
        HISTORY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        history = json.load(f)

except:

    history = []


# =====================
# Collect
# =====================

all_items = load_all_items()

# =====================
# Normalize datetime
# =====================

for item in all_items:

    if (
        item.pub_date
        and item.pub_date.tzinfo is None
    ):

        item.pub_date = item.pub_date.replace(
            tzinfo=timezone.utc
        )
        
print("===== DATETIME DEBUG =====")

print(
    "4Gamer dated:",
    sum(
        1
        for x in all_items
        if x.site == "4Gamer"
        and x.pub_date is not None
    )
)

print("===== END =====")
print()


# =====================
# Sort
# =====================

all_items.sort(
    key=lambda x: (
        x.pub_date
        or datetime.min.replace(
            tzinfo=timezone.utc
        )
    ),
    reverse=True
)


# =====================
# New Items
# =====================

new_items = [
    item
    for item in all_items
    if item.link not in history
]

all_new_items = new_items.copy()

MAX_ITEMS = 50

new_items = new_items[:MAX_ITEMS]


# =====================
# RSS
# =====================

fg = FeedGenerator()

fg.title(
    "Japanese Game Media RSS"
)

fg.link(
    href="https://www.gamespark.jp/"
)

fg.description(
    "Japanese game interview aggregation"
)

fg.language("ja")


# =====================
# RSS Entries
# =====================

for item in new_items:

    fe = fg.add_entry()

    fe.title(
        f"[{item.site}] {item.title}"
    )

    fe.link(
        href=item.link
    )

    fe.guid(
        item.link
    )

    if item.pub_date:

        fe.pubDate(
            item.pub_date
        )

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

    if item.image_url:

        fe.enclosure(
            item.image_url,
            0,
            "image/jpeg"
        )


# =====================
# Output RSS
# =====================

fg.rss_file("rss.xml")


# =====================
# Update History
# =====================

history.extend(
    item.link
    for item in all_new_items
)

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


# =====================
# Log
# =====================

print()

print(
    f"Fetched : {len(all_items)}"
)

print(
    f"New     : {len(all_new_items)}"
)

print(
    f"RSS Out : {len(new_items)}"
)

print(
    "RSS generated successfully!"
)
