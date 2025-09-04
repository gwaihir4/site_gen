from enum import Enum
from htmlnode import LeafNode  

# class TextType(Enum):
#     Plain = ""
#     Bold = ""
#     Italic = ""
#     Code = ""
#     Link = ""
#     Image = ""

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"




class TextNode():    
    # TextType = Enum('TextType', ['TEXT', 'BOLD', 'ITALIC', 'CODE', 'LINK', 'IMAGE'])
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type #TextType(text_type) 
        self.url = url
    
    def __eq__(self, other):
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        return True 

    def __repr__(self):
        return (f"TextNode({self.text}, {self.text_type.value}, {self.url})") 

def text_node_to_html_node(text_node): #text
    match text_node.text_type.value:
        case 'text':
            return LeafNode(None,text_node.text) #return LeafNode with just text
        case 'bold':
            return LeafNode("b",text_node.text)
        case 'italic':
            return LeafNode("i",text_node.text)
        case 'code':
            return LeafNode("code",text_node.text)
        case 'link':
            return LeafNode("a",text_node.text,{"href":f"{text_node.url}"})
        case 'image':
            return LeafNode("img","",{"src":f"{text_node.url}", "alt": f"{text_node.text}"})
        case _: #raise wrong text_type
            raise Exception ("Wrong TextType")