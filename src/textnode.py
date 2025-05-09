from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    """Enum for inline elements."""
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text : str, text_type : TextType = TextType.TEXT, link : str = None):
        """
        Initialize a TextNode with text, type, and optional link or image.
        Args:
            text (str): The text content of the node.
            text_type (TextType): The type of the text (normal, bold, italic, code).
            link (str): Optional link for the text.
        """
        self.text = text
        self.text_type = text_type
        self.link = link

    def __eq__(self, other):
        """
        Check equality of two TextNode objects.
        Args:
            other (TextNode): The other TextNode to compare with.
        Returns:
            bool: True if equal, False otherwise.
        """
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.link == other.link)
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.link})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.link})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.link, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")