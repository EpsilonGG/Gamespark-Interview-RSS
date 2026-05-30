from collections import Counter

from tools.utils import load_all_items


items = load_all_items()

site_counter = Counter()
category_counter = Counter()

for item in items:

    site_counter[item.site] += 1
    category_counter[item.category] += 1

print()
print("SITE")

for k, v in site_counter.items():

    print(
        f"{k}: {v}"
    )

print()
print("CATEGORY")

for k, v in category_counter.items():

    print(
        f"{k}: {v}"
    )

print()
print(
    f"TOTAL: {len(items)}"
)
