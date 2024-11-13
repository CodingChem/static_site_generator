import unittest
from ssg.modules.text_node.block import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    def test_simple_paragraph_test(self):
        paragraph_block = "this is a simple paragraph"
        expected = BlockType.PARAGRAPH
        actual = block_to_block_type(paragraph_block)
        self.assertEqual(expected, actual)

    def test_simple_quote(self):
        quote_block = """>this is a valid quote_block\n>myname"""
        expected = BlockType.QUOTE
        actual = block_to_block_type(quote_block)
        self.assertEqual(expected, actual)

    def test_ul(self):
        ul_block = "- this is a list\n* this is also"
        expected = BlockType.UNORDERED_LIST
        actual = block_to_block_type(ul_block)
        self.assertEqual(expected, actual)

    def test_ol(self):
        ol_block = "1. this is number one\n2. this is number two"
        expected = BlockType.ORDERED_LIST
        actual = block_to_block_type(ol_block)
        self.assertEqual(expected, actual)

    def test_code(self):
        code_block = r"""```this is the start
        the end ```"""
        expected = BlockType.CODE
        actual = block_to_block_type(code_block)
        self.assertEqual(expected, actual)

    def test_heading(self):
        heading = "### This is a markdown heading"
        expected = BlockType.HEADING
        actual = block_to_block_type(heading)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
