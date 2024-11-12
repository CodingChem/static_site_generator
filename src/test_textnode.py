import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Uniqe", TextType.BOLD)
        node2 = TextNode("Not me", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "test.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "test.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "test.com")
        self.assertEqual(node, node2)


class TestTextNodeToLeafNode(unittest.TestCase):
    def test_bold_text(self):
        textnode = TextNode("bold", TextType.BOLD)
        leafnode = text_node_to_html_node(textnode)
        self.assertEqual(leafnode.__repr__(), "HTMLNode(b, bold, None, None)")

    def test_just_text(self):
        textnode = TextNode("normal", TextType.TEXT)
        leafnode = text_node_to_html_node(textnode)
        self.assertEqual(leafnode.__repr__(), "HTMLNode(None, normal, None, None)")

    def test_italic(self):
        textnode = TextNode("italic", TextType.ITALIC)
        leafnode = text_node_to_html_node(textnode)
        self.assertEqual(leafnode.__repr__(), "HTMLNode(i, italic, None, None)")

    def test_code(self):
        textnode = TextNode("a = b", TextType.CODE)
        leafnode = text_node_to_html_node(textnode)
        self.assertEqual(leafnode.__repr__(), "HTMLNode(code, a = b, None, None)")

    def test_link(self):
        textnode = TextNode("mylink", TextType.LINK, ":my/url")
        leafnode = text_node_to_html_node(textnode)
        self.assertEqual(
            leafnode.__repr__(), "HTMLNode(a, mylink, None, {'href': ':my/url'})"
        )

    def test_image(self):
        textnode = TextNode("mypic", TextType.IMAGE, "mysrc")
        leafnode = text_node_to_html_node(textnode)
        self.assertEqual(
            leafnode.__repr__(),
            "HTMLNode(img, , None, {'src': 'mysrc', 'alt': 'mypic'})",
        )


if __name__ == "__main__":
    unittest.main()
