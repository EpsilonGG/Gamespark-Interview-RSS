import sys
from pathlib import Path

# 项目根目录加入 PYTHONPATH
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import importlib


if len(sys.argv) < 2:
    print("Usage: python parser_test.py parser_name")
    sys.exit(1)

parser_name = sys.argv[1]

try:

    module = importlib.import_module(
        f"parsers.{parser_name}"
    )

except Exception as e:

    print(
        f"Failed to import parser: {e}"
    )

    sys.exit(1)

if not hasattr(module, "parse"):

    print(
        f"{parser_name} has no parse()"
    )

    sys.exit(1)

items = module.parse()

print()
print("=" * 80)
print(f"Parser : {parser_name}")
print(f"Items  : {len(items)}")
print("=" * 80)

for i, item in enumerate(items[:3], start=1):

    print()
    print(f"[{i}]")
    print("SITE :", item.site)
    print("TITLE:", item.title)
    print("DATE :", item.pub_date)
    print("LINK :", item.link)
    print("IMAGE:", item.image_url)
    print("DESC :", item.description[:300])

print()
print("=" * 80)
print("TEST SUCCESS")
print("=" * 80)
