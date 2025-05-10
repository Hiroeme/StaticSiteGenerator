import sys
from generator import static_to_public, generate_pages_recursive
# print(test)

basepath = sys.argv[1] if len(sys.argv) > 1 else "/your-repo-name"

static_to_public("static", "docs")
# generate_pages_recursive("content", "template.html", "public", basepath)
generate_pages_recursive("content", "template.html", "docs", basepath)