import re
from enum import Enum
from htmlnode import HTMLNode,ParentNode,LeafNode
from textnode import text_node_to_html_node,TextNode,TextType
from inline_markdown import text_to_textnodes
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading" # (#{1,6}\s{1})
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block): # single block of markdown string (markdown_to_blocks) -> returns BlockType.?
    if len(block) == 0:
        raise Exception ("Empty Block")
    # heading
    if re.search(r"^(#{1,6}\s{1})", block):
        return BlockType.HEADING
    # code block 
    elif len(re.findall(r"(```)", block)) == 2:
        return BlockType.CODE
    # quote (every line must start with >)
    elif block[0] == ">":
        lines_in_block = block.split("\n")
        for line in lines_in_block:
            if line[0] != ">":
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    #unordered list
    elif block[0] == "-":
        lines_in_block = block.split("\n")
        for line in lines_in_block:
            if line[0] != "-":
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    #ordered list
    elif re.search(r"(^\d\.)", block[0:2]):
        start_number = int(block[0])
        lines_in_block = block.split("\n")
        for line in lines_in_block:
            if line[0:2] == f"{start_number}" + ".":
                start_number += 1
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
        
def markdown_to_blocks(markdown): # takes a markdown strings representing full document -> returns list of "block" strings
    if markdown == "":
        return []
    # Split on 1+ blank lines
    parts = re.split(r"\n\s*\n", markdown.strip())
    # Trim each block, keep non-empty
    return [p.strip() for p in parts if p.strip()]

def text_to_child(text):
    child_html_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        child_html_nodes.append(text_node_to_html_node(text_node))
    return child_html_nodes

def markdown_to_html_node(markdown):
    if len(markdown) == 0:
        raise Exception ("Empty Markdown Input")
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                text = re.sub(r"\s+", " ", block.replace("\n", " ")).strip()
                child_nodes = text_to_child(text)
                current_block = ParentNode("p", child_nodes)
            case BlockType.HEADING:
                capture = re.match(r"^(#{1,6}\s{1})", block)
                prefix = capture.group(1)
                level = prefix.count("#")
                text = block[len(prefix):]
                child_nodes = text_to_child(text)
                current_block = ParentNode(f"h{level}", child_nodes)
            case BlockType.CODE:
                lines = block.split("\n")
                # validate fences on their own lines
                if not (lines and lines[0].lstrip().startswith("```") and lines[-1].lstrip().startswith("```")):
                    raise ValueError("invalid code block")

                # remove fence lines
                inner_lines = lines[1:-1]

                # dedent common leading spaces
                def common_indent(ss):
                    indents = [len(s) - len(s.lstrip(" ")) for s in ss if s.strip() != ""]
                    return min(indents) if indents else 0

                indent = common_indent(inner_lines)
                dedented = [s[indent:] if len(s) >= indent else s for s in inner_lines]

                inner_text = "\n".join(dedented)
                if not inner_text.endswith("\n"):
                    inner_text += "\n"
            
                # one <code> only, no inline parsing beyond being a code LeafNode
                code_leaf = text_node_to_html_node(TextNode(inner_text, TextType.CODE))  # should be LeafNode("code", ...)
                current_block = ParentNode("pre", [code_leaf])
            case BlockType.QUOTE:
                lines = []
                for line in block.split("\n"):
                    s = line.lstrip()
                    if s.startswith("> "):
                        lines.append(s[2:])
                    elif s.startswith(">"):
                        lines.append(s[1:])
                    else:
                        lines.append(s)  # or skip, depending on your spec
                text = " ".join(lines)  # or "\n".join(lines) if you want newlines
                child_nodes = text_to_child(text)
                current_block = ParentNode("blockquote", child_nodes)
            case BlockType.UNORDERED_LIST:
                items = []
                for line in block.split("\n"):
                    line = line.lstrip()
                    if line.startswith("- ") or line.startswith("* "):
                        item_text = line[2:]
                        items.append(ParentNode("li", text_to_child(item_text)))
                current_block = ParentNode("ul", items)
            case BlockType.ORDERED_LIST:
                items = []
                for line in block.split("\n"):
                    line = line.lstrip()
                    m = re.match(r"^\d+\.\s+(.*)$", line)
                    if m:
                        items.append(ParentNode("li", text_to_child(m.group(1))))
                current_block = ParentNode("ol", items)
            case _:
                raise Exception ("Error handling BlockType (Wrong Block Type)")
        block_nodes.append(current_block)
    return ParentNode("div", block_nodes)

def extract_title(markdown):
    if markdown.startswith("# "):
        title = markdown.split("\n")[0]
        return title
    raise Exception ("H1 title not found")

