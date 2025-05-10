import unittest
from generator import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        md = "# title"
        title = extract_title(md)

        self.assertEqual("title", title)

    def test_extract_multiline_title(self):
        md = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)"""
        title = extract_title(md)

        self.assertEqual("Tolkien Fan Club", title)

if __name__ == "__main__":
    unittest.main()