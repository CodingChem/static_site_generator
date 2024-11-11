import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_have_leading_space(self):
        node = HTMLNode(props={"href": "mylink"})
        self.assertEqual(node.props_to_html(), ' href="mylink"')

    def test_props_to_html_have_leading_spaces(self):
        node = HTMLNode(props={"href": "mylink", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="mylink" target="_blank"')


if __name__ == "__main__":
    unittest.main()
