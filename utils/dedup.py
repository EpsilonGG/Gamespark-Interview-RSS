def remove_duplicates(items):
    seen = set()
    unique_items = []

    for item in items:
        key = item.link

        if key not in seen:
            seen.add(key)
            unique_items.append(item)

    return unique_items
