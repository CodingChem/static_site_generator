import unittest
from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_handles_singe_bold(self):
        nodes = [TextNode("text with *bold* subnode", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" subnode", TextType.TEXT),
            ],
        )

    def test_handles_multiple_bold(self):
        nodes = [TextNode("text *with* bold *subnode*", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("text ", TextType.TEXT),
                TextNode("with", TextType.BOLD),
                TextNode(" bold ", TextType.TEXT),
                TextNode("subnode", TextType.BOLD),
            ],
        )

    def test_handles_bold_first(self):
        nodes = [TextNode("*I* am a bold text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("I", TextType.BOLD),
            TextNode(" am a bold text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_first_then_multiple_and_sequential(self):
        nodes = [
            TextNode("*starting* with *bold* and continuing *with* *it*", TextType.TEXT)
        ]
        actual = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("starting", TextType.BOLD),
            TextNode(" with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and continuing ", TextType.TEXT),
            TextNode("with", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("it", TextType.BOLD),
        ]
        self.assertEqual(actual, expected)

    def test_no_delimiter_in_text_raises(self):
        nodes = [TextNode("nothing to see here", TextType.TEXT)]
        self.assertRaises(
            ValueError, lambda: split_nodes_delimiter(nodes, "*", TextType.BOLD)
        )


if __name__ == "__main__":
    unittest.main()
