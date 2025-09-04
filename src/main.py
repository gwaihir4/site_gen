from textnode import TextNode, TextType

def main():
    new_node = TextNode("this is a plain text", TextType.BOLD)
    new_node2 = TextNode ("text number 2 ", TextType.LINK, "www.google.com")
    print (new_node)
    print (new_node2)

main()