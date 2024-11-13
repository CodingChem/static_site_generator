import unittest

from ssg.modules.html_node import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leafnode_renders_simple_text(self):
        node = LeafNode(tag=None, value="simple text")
        self.assertEqual(node.to_html(), "simple text")

    def test_leafnode_renders_paragraph(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leafnode_renders_link_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_empty_leaf_value_raises(self):
        node = LeafNode(None, None)  # pyright: ignore
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()
