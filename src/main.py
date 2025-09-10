import sys
from build_public import build_public
from generate_page import generate_pages_recursive
def main():
    if  len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    build_public("static","docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
if __name__ == "__main__":
    main()