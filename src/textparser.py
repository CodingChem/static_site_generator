import re

from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    strings = markdown.split("\n\n")
    for line in strings:
        if line.strip() == "":
            continue
        blocks.append(line.strip())
    return blocks


def text_to_textnode(text: str) -> list[TextNode]:
    # do bold before italics to avoid collisions,
    # similarly do images before links.
    textnode = TextNode(text, TextType.TEXT)
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
