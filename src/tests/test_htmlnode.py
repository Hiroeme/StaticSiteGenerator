import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from htmlnode import HtmlNode

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

