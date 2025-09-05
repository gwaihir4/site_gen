import re
from textnode import TextNode,TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if len(old_nodes) == None:
        return new_nodes
    for old_node in old_nodes:
        if old_node.text_type.value != 'text':
            new_nodes.append(old_node)
            continue
        else:
            parts = old_node.text.split(f"{delimiter}")
            # tmp.append(old_node.text.split(f"{delimiter}"))
            if len(parts) == 1:
                new_nodes.append(old_node)
                # raise Exception ("Delimitter not found in text")
            elif len(parts) % 2 == 0:
                raise Exception ("Cant find closing delimitter")
            elif len(parts) % 2 == 1:
                for i in range (len(parts)):
                    if parts[i] == "":
                        continue
                    if i % 2 == 0:
                        new_nodes.append(TextNode(parts[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes

def extract_markdown_images(text):
# text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    capture = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return capture

def extract_markdown_links(text):
    capture = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return capture

def split_nodes_image(old_nodes):
    new_nodes =[]
    if len(old_nodes) == 0 : # if input is empty return empty list
        return []
    for old_node in old_nodes: # for every node
        if old_node.text_type != TextType.TEXT: # if node is not textnode append dont process
            new_nodes.append(old_node)
            continue
        else:
            image_captures = extract_markdown_images(old_node.text)
            if image_captures == []: # if image is not found in text append as textnode
                new_nodes.append(old_node)
                continue
            remaining = old_node.text # our remaining part of the text for initial setup
            for image_capture in image_captures: # for every image captured in node.text
                markdown_str = f"![{image_capture[0]}]({image_capture[1]})"
                parts = remaining.split(markdown_str, 1)
                before_part = parts[0]
                after_part = parts[1]
                if before_part != "": # if part before split is not empty
                    new_nodes.append(TextNode(before_part, TextType.TEXT))
                    new_nodes.append(TextNode(image_capture[0],TextType.IMAGE,image_capture[1]))
                else: # if part before split is empty
                    new_nodes.append(TextNode(image_capture[0],TextType.IMAGE,image_capture[1]))
                remaining = after_part # update the remaining part
            if remaining != "": # if there is still text left in remaining after the loop add it as textnode
                new_nodes.append(TextNode(remaining,TextType.TEXT))
    return new_nodes
def split_nodes_link(old_nodes):
    new_nodes =[]
    if len(old_nodes) == 0 : # if input is empty return empty list
        return []
    for old_node in old_nodes: # for every node
        if old_node.text_type != TextType.TEXT: # if node is not textnode append dont process
            new_nodes.append(old_node)
            continue
        else:
            link_captures = extract_markdown_links(old_node.text)
            if link_captures == []: # if link is not found in text append as textnode
                new_nodes.append(old_node)
                continue
            remaining = old_node.text # our remaining part of the text for initial setup
            for link_capture in link_captures: # for every link captured in node.text
                markdown_str = f"[{link_capture[0]}]({link_capture[1]})" # there is no ! mark in the start of markdown_str
                parts = remaining.split(markdown_str, 1)
                before_part = parts[0]
                after_part = parts[1]
                if before_part != "": # if part before split is not empty
                    new_nodes.append(TextNode(before_part, TextType.TEXT))
                    new_nodes.append(TextNode(link_capture[0],TextType.LINK,link_capture[1]))
                else: # if part before split is empty
                    new_nodes.append(TextNode(link_capture[0],TextType.LINK,link_capture[1]))
                remaining = after_part # update the remaining part
            if remaining != "": # if there is still text left in remaining after the loop add it as textnode
                new_nodes.append(TextNode(remaining,TextType.TEXT))
    return new_nodes

def text_to_textnode(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    delimiters = ["_", "**", "`", ]
    if text == "" or None:
        return []
    else:
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        new_nodes = split_nodes_image(new_nodes)
        new_nodes = split_nodes_link(new_nodes)
    return new_nodes