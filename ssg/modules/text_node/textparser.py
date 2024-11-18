import re

from modules.html_node.parentnode import ParentNode
from .block import BlockType, block_to_block_type, markdown_to_blocks

from .split_nodes import split_nodes_delimiter
from .textnode import TextNode, TextType


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No h1 in file!")


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                text_nodes = text_to_textnode(block)
                nodes.append(
                    ParentNode("p", [x.text_node_to_html_node() for x in text_nodes])
                )
            case BlockType.HEADING:
                words = block.split(" ")
                heading_level = len(words.pop(0))
                text_nodes = text_to_textnode(" ".join(words))
                nodes.append(
                    ParentNode(
                        f"h{heading_level}",
                        [x.text_node_to_html_node() for x in text_nodes],
                    )
                )
            case BlockType.CODE:
                text_nodes = text_to_textnode(block.replace("```", "")[1:-1])
                nodes.append(
                    ParentNode("code", [x.text_node_to_html_node() for x in text_nodes])
                )
            case BlockType.QUOTE:
                text_nodes = text_to_textnode(block.replace(">", ""))
                nodes.append(
                    ParentNode(
                        "blockquote", [x.text_node_to_html_node() for x in text_nodes]
                    )
                )
            case BlockType.UNORDERED_LIST:
                children = []
                for line in block.replace("- ", "* ").split("* "):
                    line = line.strip()
                    if line == "":
                        continue
                    children.append(
                        ParentNode(
                            "li",
                            [
                                x.text_node_to_html_node()
                                for x in text_to_textnode(line)
                            ],
                        )
                    )
                nodes.append(ParentNode("ul", children))
            case BlockType.ORDERED_LIST:
                children = []
                for line in re.split(r"\d+\.\s", block):
                    if line[2:] == "":
                        continue
                    children.append(
                        ParentNode(
                            "li",
                            [
                                x.text_node_to_html_node()
                                for x in text_to_textnode(line)
                            ],
                        )
                    )
                nodes.append(ParentNode("ol", children))

    return ParentNode("body", nodes)


def text_to_textnode(text: str) -> list[TextNode]:
    # do bold before italics to avoid collisions,
    # similarly do images before links.
    textnode = TextNode(text.strip(), TextType.TEXT)
    return split_nodes_link(
        split_nodes_images(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([textnode], "**", TextType.BOLD),
                    "*",
                    TextType.ITALIC,
                ),
                "`",
                TextType.CODE,
            )
        )
    )


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex, text)


def split_nodes_link(nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in nodes:
        new_nodes.extend(_split_node_link(node))
    return new_nodes


def split_nodes_images(nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in nodes:
        new_nodes.extend(_split_node_image(node))
    return new_nodes


def _split_node_link(node: TextNode) -> list[TextNode]:
    text = node.text
    links = extract_markdown_links(node.text)
    if len(links) < 1 and len(text) < 1:
        return []
    if len(links) < 1:
        return [node]
    preceding, following = text.split(f"[{links[0][0]}]({links[0][1]})")
    match (preceding, following):
        case ("", ""):
            return [TextNode(links[0][0], TextType.LINK, links[0][1])]

        case (x, "") if isinstance(x, str):
            return [
                TextNode(x, TextType.TEXT),
                TextNode(links[0][0], TextType.LINK, links[0][1]),
            ]

        case ("", x) if isinstance(x, str):
            return [
                TextNode(links[0][0], TextType.LINK, links[0][1]),
            ] + _split_node_link(TextNode(x, TextType.TEXT))

        case (x, y) if isinstance(x, str) and isinstance(y, str):
            return [
                TextNode(x, TextType.TEXT),
                TextNode(links[0][0], TextType.LINK, links[0][1]),
            ] + _split_node_link(TextNode(y, TextType.TEXT))
        case _:
            raise Exception("you missed a case!")


def _split_node_image(node: TextNode) -> list[TextNode]:
    text = node.text
    links = extract_markdown_images(node.text)
    if len(links) < 1 and len(text) < 1:
        return []
    if len(links) < 1:
        return [node]
    preceding, following = text.split(f"![{links[0][0]}]({links[0][1]})")
    match (preceding, following):
        case ("", ""):
            return [TextNode(links[0][0], TextType.IMAGE, links[0][1])]

        case (x, "") if isinstance(x, str):
            return [
                TextNode(x, TextType.TEXT),
                TextNode(links[0][0], TextType.IMAGE, links[0][1]),
            ]

        case ("", x) if isinstance(x, str):
            return [
                TextNode(links[0][0], TextType.IMAGE, links[0][1]),
            ] + _split_node_image(TextNode(x, TextType.TEXT))

        case (x, y) if isinstance(x, str) and isinstance(y, str):
            return [
                TextNode(x, TextType.TEXT),
                TextNode(links[0][0], TextType.IMAGE, links[0][1]),
            ] + _split_node_image(TextNode(y, TextType.TEXT))
        case _:
            raise Exception("you missed a case!")
