from build_public import build_public
from generate_page import generate_pages_recursive
def main():
    build_public("static")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()