import importlib
import pkgutil

import parsers


def debug_parser(module_name):

    print()
    print("=" * 60)
    print(f"[Parser] {module_name}")
    print("=" * 60)

    try:

        module = importlib.import_module(
            f"parsers.{module_name}"
        )

        if not hasattr(module, "parse"):

            print("No parse() found")

            return

        items = module.parse()

        print(
            f"Items fetched: {len(items)}"
        )

        if not items:

            print("No items returned")

            return

        item = items[0]

        print()
        print("First item:")
        print(f"site       : {item.site}")
        print(f"category   : {item.category}")
        print(f"title      : {item.title}")
        print(f"link       : {item.link}")
        print(f"pub_date   : {item.pub_date}")
        print(f"image_url  : {item.image_url}")
        print(type(item.pub_date))
        print(item.pub_date.tzinfo)

        desc = item.description or ""

        if len(desc) > 200:
            desc = desc[:200] + "..."

        print(f"description: {desc}")

    except Exception as e:

        print(
            f"ERROR: {e}"
        )


def main():

    print()
    print("RSS Parser Debug")
    print()

    for module_info in pkgutil.iter_modules(
        parsers.__path__
    ):

        debug_parser(
            module_info.name
        )


if __name__ == "__main__":

    main()
