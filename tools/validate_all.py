from collections import Counter

from tools.utils import load_all_items


items = load_all_items()

print()
print("VALIDATION")
print("=" * 50)

links = []

for item in items:

    if not item.title:

        print(
            f"[EMPTY TITLE] {item.site}"
        )

    if not item.link:

        print(
            f"[EMPTY LINK] {item.site}"
        )

    links.append(
        item.link
    )

counter = Counter(
    links
)

for link, count in counter.items():

    if count > 1:

        print(
            f"[DUPLICATE] {count}x {link}"
        )

print()
print(
    f"Total: {len(items)}"
)
