import sys
import json

from tools.utils import load_parser


def main():

    parser_name = sys.argv[1]

    parser = load_parser(
        parser_name
    )

    items = parser.parse()

    output = []

    for item in items:

        output.append(
            {
                "site": item.site,
                "category": item.category,
                "title": item.title,
                "link": item.link,
                "description": item.description,
                "image_url": item.image_url,
                "pub_date": (
                    item.pub_date.isoformat()
                    if item.pub_date
                    else None
                ),
                "tags": item.tags
            }
        )

    with open(
        f"dump/{parser_name}.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output,
            f,
            ensure_ascii=False,
            indent=2
        )


if __name__ == "__main__":
    main()
