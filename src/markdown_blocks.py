from enum import Enum

from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_node_to_html_node, text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def text_to_children(text):
    # collapse all multispaces into one space.
    text = " ".join(text.split())
    textnodes = text_to_textnodes(text)
    htmlnodes = []
    for textnode in textnodes:
        htmlnodes.append(text_node_to_html_node(textnode))
    return htmlnodes

def olist_text_to_children(text):
    # collapse all multispaces into one space.
    split_text = text.split("\n")
    
    i = 1
    list_items = []
    for t in split_text:
        # if not t.strip():
        #     continue
        t = t.replace(f"{i}. ", "")
        textnodes = text_to_textnodes(t)

        item_children = []
        for textnode in textnodes:
            item_children.append(text_node_to_html_node(textnode))

        list_items.append(item_children)
        i += 1
    return list_items

def ulist_text_to_children(text):
    split_text = text.split("\n")
    list_items = []
    
    for line in split_text:
        # if not line.strip():
        #     continue

        line = line.replace("- ", "", 1)
        textnodes = text_to_textnodes(line)
        
        # Create HTML nodes for this line
        item_children = []
        for textnode in textnodes:
            item_children.append(text_node_to_html_node(textnode))
        
        # Add this line as one list item
        list_items.append(item_children)
        
    return list_items

def bquote_text_to_children(text):
    split_text = text.split("\n")

    for i in range(len(split_text)):
        split_text[i] = split_text[i].replace(">", "", 1).strip()
    
    text = " ".join(split_text)

    list_items = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        list_items.append(text_node_to_html_node(textnode))
    return list_items

def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    
    children = []
    for block in blocks:
        if len(block) == 0:
            continue
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                parent = ParentNode("p", text_to_children(block))
                children.append(parent)
            case BlockType.HEADING:
                heading = "h1"
                if block.startswith("## "):
                    heading = "h2"
                    block = block.replace("## ", "", 1)
                if block.startswith("### "):
                    heading = "h3"
                    block = block.replace("### ", "", 1)
                if block.startswith("#### "):
                    heading = "h4"
                    block = block.replace("#### ", "", 1)
                if block.startswith("##### "):
                    heading = "h5"
                    block = block.replace("##### ", "", 1)
                if block.startswith("###### "):
                    heading = "h6"
                    block = block.replace("###### ", "", 1)
                block = block.replace("# ", "", 1)
                parent = ParentNode(heading, text_to_children(block))
                children.append(parent)
            case BlockType.CODE:
                block = block[3:-3].lstrip('\n')
                parent = ParentNode("pre", [text_node_to_html_node(TextNode(block, TextType.CODE))])
                children.append(parent)
            case BlockType.QUOTE:
                parent = ParentNode("blockquote", bquote_text_to_children(block))
                children.append(parent)
            case BlockType.OLIST:
                nodes = olist_text_to_children(block)
                list_items = []
                for item_group in nodes:
                    list_items.append(ParentNode("li", item_group))
                parent = ParentNode("ol", list_items)
                children.append(parent)
            case BlockType.ULIST:
                item_groups = ulist_text_to_children(block)
                list_items = []
                for item_group in item_groups:
                    list_items.append(ParentNode("li", item_group))
                parent = ParentNode("ul", list_items)
                children.append(parent)

        # print(children)
    return ParentNode("div", children)