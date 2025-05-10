from generator import static_to_public, generate_pages_recursive
# print(test)

static_to_public("static", "public")
generate_pages_recursive("content", "template.html", "public")