import sys
from generator import static_to_public, generate_pages_recursive
# print(test)

basepath = sys.argv[0] if sys.argv else "/"

static_to_public("static", "docs")
# generate_pages_recursive("content", "template.html", "public", basepath)
generate_pages_recursive("content", "template.html", "docs", basepath)