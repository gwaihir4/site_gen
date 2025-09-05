import unittest

from textnode import TextNode, TextType,text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)      

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.CODE, None)
        node2 = TextNode("This is a text node", TextType.LINK, "")
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node1", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_html_node(self):
        node = TextNode("test text for html", TextType.TEXT)
        html_node = HTMLNode("h1", "hey this is a value for html tag", node,{"href": "https://www.google.com"})
        # print (html_node)
        # print (html_node.props_to_html())

        node = TextNode("test text for html", TextType.TEXT)
        html_node = HTMLNode("h1", "hey this is a value for html tag", node,{"href": "https://www.google.com", "target": "_blank"})
        # print (html_node)
        # print (html_node.props_to_html())

    def test_leaf_to_html_p(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com", "tag": "-blank"})
        #print(node.to_html())
        self.assertNotEqual(node.to_html(), "<p>Hello, world!</p>")

        node = LeafNode("p", "Hello, world!")
        #print(node.to_html())
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
 
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_text(self): # Plain Text 
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text2(self): # Code Block
        node = TextNode("Code Block", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code Block")
    def test_text3(self): # Link 
        node = TextNode("Click Here", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click Here")
        self.assertEqual(html_node.props["href"], "www.google.com")
    def test_text3(self): # Image
        node = TextNode("Image explanation", TextType.IMAGE, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "www.google.com")
        self.assertEqual(html_node.props["alt"], "Image explanation")
    def test_split_nodes_italic_simple(self):
        input_nodes = [TextNode("This _is a text_ node", TextType.TEXT)]
        result = split_nodes_delimiter(input_nodes, "_", TextType.ITALIC)

        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("is a text", TextType.ITALIC),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
if __name__ == "__main__":
    unittest.main()
