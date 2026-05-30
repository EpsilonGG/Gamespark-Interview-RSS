import pkgutil
import importlib

import parsers


def load_all_items():

    items = []

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

        except Exception as e:

            print(
                f"[ERROR] {module_name}: {e}"
            )

    return items


def load_parser(name):

    module = importlib.import_module(
        f"parsers.{name}"
    )

    return module
