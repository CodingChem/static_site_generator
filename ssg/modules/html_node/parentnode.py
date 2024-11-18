from .htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict | None = None,
    ) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode *must* have a tag")
        if self.children is None or len(self.children) < 1:
            raise ValueError("ParentNode *must* have children")
        return (
            f"<{self.tag}{self.props_to_html()}>"
            + "".join([x.to_html() for x in self.children])
            + f"</{self.tag}>\n"
        )
