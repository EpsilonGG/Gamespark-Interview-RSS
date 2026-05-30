from tools.utils import load_all_items

items = load_all_items()

items.sort(
    key=lambda x: (
        x.pub_date
        if x.pub_date
        else 0
    ),
    reverse=True
)

print()

for item in items[:30]:

    print(
        f"[{item.site}]"
    )

    print(item.title)

    print(item.link)

    print("-" * 60)
