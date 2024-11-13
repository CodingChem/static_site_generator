from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    strings = markdown.split("\n\n")
    for line in strings:
        if line.strip() == "":
            continue
        blocks.append(line.strip())
    return blocks


def block_to_block_type(block: str) -> BlockType:
    re_heading = r"^#+\s"
    re_code_block = r"^```[\S|\s]*?```$"
    re_ul = r"^(?:[-*].*\n?)+$"
    re_ol = r"^(?:\d+\. .+\n?)+$"
    re_qoute = r"^(?:>.*\n?)+$"
    lines = list(filter(lambda x: len(x) < 1, block.split("\n")))
    if len(lines) < 2 and re.match(re_heading, block):
        return BlockType.HEADING
    if re.match(re_code_block, block):
        return BlockType.CODE
    if re.match(re_ul, block):
        return BlockType.UNORDERED_LIST
    if re.match(re_ol, block):
        return BlockType.ORDERED_LIST
    if re.match(re_qoute, block):
        return BlockType.QUOTE
    return BlockType.PARAGRAPH
