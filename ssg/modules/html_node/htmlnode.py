from __future__ import annotations


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, self.__class__):
            return False
        return (
            self.tag == value.tag
            and self.value == value.value
            and self.children == value.children
            and self.props == value.props
        )

    def props_to_html(self):
        if self.props is None:
            return ""
        return " " + " ".join([f'{k}="{v}"' for k, v in self.props.items()])

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
