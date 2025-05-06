import unittest

from htmlnode import HtmlNode, LeafNode

class TestHtmlNode(unittest.TestCase):

    def test_eq_props(self):
        node = HtmlNode(props={
                "href": "https://www.google.com",
                "target": "_blank",
            })
        node2 = HtmlNode(props={
                "href": "https://www.google.com",
                "target": "_blank",
            })
        
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_eq_diff_props(self):
        node = HtmlNode(props={
                "href": "https://www.google.com",
                "target": "_blankss",
            })
        node2 = HtmlNode(props={
                "href": "https://www.google.com",
                "target": "_blank",
            })
        
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())

    def test_eq_no_props(self):
        node = HtmlNode()
        node2 = HtmlNode()
        
        self.assertEqual(node.props_to_html(), node2.props_to_html())


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_no_value(self):
        node = LeafNode(None, None, None)
        try:
            node.to_html()
        except ValueError as e:
            self.assertEqual(str(e),"All leaf nodes must have a value")