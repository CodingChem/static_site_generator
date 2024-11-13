from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    new_nodes = []
    for node in old_nodes:
        sub_nodes = []
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splits = node.text.split(delimiter)
        if len(splits) < 1:
            new_nodes.append(node)
            continue
        for index, split in enumerate(splits, start=1):
            if split == "":
                continue
            if iseven(index):
                sub_nodes.append(TextNode(split, text_type))
            else:
                sub_nodes.append(TextNode(split, TextType.TEXT))
        new_nodes.extend(sub_nodes)
    if len(new_nodes) == len(old_nodes):
        raise ValueError("seperator not found in text")
    return new_nodes


def iseven(num: int):
    return num % 2 == 0
