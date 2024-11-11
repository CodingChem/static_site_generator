import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [])  # pyright: ignore
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_empty_children_raises(self):
        node = ParentNode("a", [])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_None_children_raises(self):
        node = ParentNode("a", None)  # pyright: ignore
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_provided_example_works(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )


if __name__ == "__main__":
    unittest.main()
