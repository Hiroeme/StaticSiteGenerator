
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
        return " " + " ".join([f'{key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self):
        print(self.tag, self.value, self.children, self.props)
