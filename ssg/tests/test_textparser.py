import unittest
from ssg.modules.html_node.leafnode import LeafNode
from ssg.modules.html_node.parentnode import ParentNode
from ssg.modules.text_node.textnode import TextType, TextNode

from ssg.modules.text_node.block import markdown_to_blocks
from ssg.modules.text_node.textparser import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
    markdown_to_html_node,
    split_nodes_link,
    split_nodes_images,
    text_to_textnode,
)


class TestExtractTitle(unittest.TestCase):
    def test_find_simple_title(self):
        markdown = "# Hello"
        expected = "Hello"
        actual = extract_title(markdown)
        self.assertEqual(expected, actual)

    def test_find_simple_title_in_larger_markdown(self):
        markdown = """
# Hello

this is a longer block
"""
        expected = "Hello"
        actual = extract_title(markdown)
        self.assertEqual(expected, actual)

    def test_title_is_not_first_block(self):
        markdown = """
granted this is wierdly formatted markdown,
but here comes the:

# Title"""
        expected = "Title"
        actual = extract_title(markdown)
        self.assertEqual(expected, actual)

    def test_no_title_raises(self):
        markdown = "there is no title here"
        self.assertRaises(Exception, lambda: extract_title(markdown))


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraph_block(self):
        markdown = """
1

2
"""
        expected = ParentNode(
            "body",
            [
                ParentNode("p", [LeafNode(None, "1")]),
                ParentNode("p", [LeafNode(None, "2")]),
            ],
        )
        actual = markdown_to_html_node(markdown)
        self.assertEqual(expected, actual)

    def test_heading_block(self):
        markdown = """
# heading with *formatting*

## subheading with multiple words
"""
        expected = ParentNode(
            "body",
            [
                ParentNode(
                    "h1", [LeafNode(None, "heading with "), LeafNode("i", "formatting")]
                ),
                ParentNode("h2", [LeafNode(None, "subheading with multiple words")]),
            ],
        )
        actual = markdown_to_html_node(markdown)
        self.assertEqual(expected, actual)

    def test_code_block(self):
        markdown = """
```
int i = 69;
```
"""
        expected = ParentNode(
            "body", [ParentNode("code", [LeafNode(None, "int i = 69;")])]
        )
        actual = markdown_to_html_node(markdown)
        self.assertEqual(expected, actual)

    def test_quote_block(self):
        markdown = """
>It is better to have lived
>Than not"""
        expected = ParentNode(
            "body",
            [
                ParentNode(
                    "blockquote",
                    [LeafNode(None, "It is better to have lived\nThan not")],
                )
            ],
        )
        actual = markdown_to_html_node(markdown)
        self.assertEqual(expected, actual)

    def test_ordered_list(self):
        markdown = """
1. first
2. second
"""
        expected = ParentNode(
            "body",
            [
                ParentNode(
                    "ol",
                    [
                        ParentNode("li", [LeafNode(None, "first")]),
                        ParentNode("li", [LeafNode(None, "second")]),
                    ],
                )
            ],
        )
        actual = markdown_to_html_node(markdown)
        self.assertEqual(expected, actual)

    def test_unordered_list(self):
        markdown = """
- first
* second
"""
        expected = ParentNode(
            "body",
            [
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode(None, "first")]),
                        ParentNode("li", [LeafNode(None, "second")]),
                    ],
                )
            ],
        )
        actual = markdown_to_html_node(markdown)
        self.assertEqual(expected, actual)


class TestExtractMarkdownImage(unittest.TestCase):
    def test_provided_test_case(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        actual = extract_markdown_images(text)

        self.assertEqual(expected, actual)


class TestExtractMarkdownLink(unittest.TestCase):
    def test_provided_test_case(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        actual = extract_markdown_links(text)
        self.assertEqual(expected, actual)


class TestSplitNodesLinks(unittest.TestCase):
    def test_provided_test_case(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        actual = split_nodes_link([node])

        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(expected, actual)


class TestSplitNodesImages(unittest.TestCase):
    def test_provided_test_case(self):
        node = TextNode(
            "This is text with a image ![my image](src/image1) and ![second image](src/image2)",
            TextType.TEXT,
        )
        actual = split_nodes_images([node])

        expected = [
            TextNode("This is text with a image ", TextType.TEXT),
            TextNode("my image", TextType.IMAGE, "src/image1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "src/image2"),
        ]
        self.assertEqual(expected, actual)


class TestTextToTextNode(unittest.TestCase):
    def test_provided(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual = text_to_textnode(text)
        self.assertEqual(expected, actual)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_provided(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
            """
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
* This is a list item
* This is another list item""",
        ]
        actual = markdown_to_blocks(text)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
