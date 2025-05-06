
class HtmlNode():
    """A class representing a node in an HTML document tree."""

    def __init__(self, tag: str = None, value : str = None, children : list = None, props : dict = None):
        """
        Initialize an HtmlNode with a tag, value, children, and properties.
        Args:
            tag (str): The HTML tag of the node.
            value (str): The text content of the node.
            children (list): Optional list of child nodes.
            props (dict): Optional dictionary of properties for the node.
        """
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def props_to_html(self):
        """
        Convert the properties of the node to an HTML string.
        Returns:
            str: The HTML string representation of the properties.
        """
        if not self.props:
            return ""
        return " " + " ".join([f'{key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HtmlNode):

    def __init__(self, tag = None, value = None, props = None):
        if not value:
            raise ValueError("All leaf nodes must have a value")

        super().__init__(tag, value, None, props)
        

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        if not tag:
            raise ValueError("All Parent nodes must have a tag")
        if not children:
            raise ValueError("All Parent nodes must have children")
        
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All Parent nodes must have a tag")
        if not self.children:
            raise ValueError("All Parent nodes must have children")
        
        return f"<{self.tag}{self.props_to_html()}>{"".join([x.to_html() for x in self.children])}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"