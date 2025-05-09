import re
from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node : TextNode):
    
    match text_node.text_type:

        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href" : text_node.link})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.link, "alt": text_node.text})
        case _:
            raise ValueError("Incorrect arguements for TextNode")
        
def split_nodes_delimiter(old_nodes : list[TextNode], delimiter, text_type):
    
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type.TEXT:
            new_nodes.append(old_node)
            continue
        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("Invalid markdown syntax")
        
        valid_nodes = []
        # # len 3?
        # if len(split_text[0]) != 0:
        #     new_nodes.append(TextNode(split_text[0], TextType.TEXT))
        # if len(split_text[1]) != 0:
        #     new_nodes.append(TextNode(split_text[1], text_type))
        # if len(split_text[2]) != 0:
        #     new_nodes.append(TextNode(split_text[2], TextType.TEXT))
        for i in range(len(split_text)):
            if len(split_text[i]) == 0:
                continue
            if i % 2 == 0:
                valid_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                valid_nodes.append(TextNode(split_text[i], text_type))
        
        new_nodes.extend(valid_nodes)
        
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes : list[TextNode]):
    new_nodes = []
    
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue        
        if not images:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text

        for alt_text, link in images:
            sections = text.split(f"![{alt_text}]({link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if len(sections[0]) == 0:
                text = sections[1]
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, link))
                continue

            text = sections[1]
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, link))
        if len(text) != 0:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue        
        if not links:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text

        for link_text, link in links:
            sections = text.split(f"[{link_text}]({link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if len(sections[0]) == 0:
                text = sections[1]
                new_nodes.append(TextNode(link_text, TextType.LINK, link))
                continue

            text = sections[1]
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link))
        if len(text) != 0:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
