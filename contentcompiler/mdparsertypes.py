from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self
from os.path import splitext

_media_base_path = "media/"
_external_media_base_path = "https://lprod.dev/blog/media/"


class Node(ABC):

    @abstractmethod
    def dump(self: Self, indent: int = 0) -> str:
        pass


@dataclass
class Tree:
    children: list[Node]

    def dump(self: Self) -> str:
        out = ""
        for child in self.children:
            out += child.dump(0)
        return out

    def html(self: Self, external: bool = False) -> str:
        out = "<html>\n"
        for child in self.children:
            out += child.html(external)
        return out + "\n</html>\n"

# Block Nodes


@dataclass
class ParagraphNode(Node):
    children: list[Node]

    def dump(self: Self, indent: int) -> str:
        out = (" " * 4 * indent) + "Paragraph Node\n"
        for child in self.children:
            # print(child, type(child))
            out += child.dump(indent + 1)
        return out

    def html(self: Self, external: bool) -> str:
        out = "<p>"
        for child in self.children:
            out += child.html(external)
        return out + "</p>\n\n"


@dataclass
class CodeBlockNode(Node):
    children: list[Node]

    def dump(self: Self, indent: int) -> str:
        out = (" " * 4 * indent) + "Code Block Node\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out

    def html(self: Self, external: bool) -> str:
        out = "<pre>\n"
        for child in self.children:
            out += child.html(external).strip()
            # WARNING does strip have side effects here?
        return out + "\n</pre>\n"


@dataclass
class ListBlockNode(Node):
    children: list[Node]
    type: str = "unordered"

    def dump(self: Self, indent: int) -> str:
        out = (" " * 4 * indent) + "List Block Node\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out

    def html(self: Self, external: bool) -> str:
        out = ""
        if self.type == "unordered":
            out = "<ul>\n"
            for child in self.children:
                out += child.html(external)
        return out + "\n</ul>\n"

# Inline Nodes


@dataclass
class HeaderNode(Node):
    children: list[Node]
    level: int

    def dump(self: Self, indent: int) -> str:
        out = (" " * 4 * indent) + f"Header Node: Level {self.level}\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out

    def html(self: Self, external: bool) -> str:
        out = f"<h{self.level}>"
        for child in self.children:
            out += child.html(external)
        return out + f"</h{self.level}>\n\n"


@dataclass
class InlineCodeNode(Node):
    children: list[Node]

    def dump(self: Self, indent: int) -> str:
        out = (" " * 4 * indent) + "Inline Code Node\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out

    def html(self: Self, external: bool) -> str:
        out = "<code>"
        for child in self.children:
            out += child.html(external)
        return out + "</code>"


@dataclass
class ListElementNode(Node):
    children: list[Node]

    def dump(self: Self, indent: int) -> str:
        out = (" " * 4 * indent) + "List Element Node\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out

    def html(self: Self, external: bool) -> str:
        out = "<li>"
        for child in self.children:
            out += child.html(external)
        return out + "</li>"


@dataclass
class StrikethroughNode(Node):
    children: list[Node]

    def dump(self: Self, indent: int) -> str:
        out = (" " * 4 * indent) + "Strikethrough Node\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out

    def html(self: Self, external: bool) -> str:
        out = "<s>"
        for child in self.children:
            out += child.html(external)
        return out + "</s>"


@dataclass
class ItalicsNode(Node):
    children: list[Node]

    def dump(self: Self, indent: int) -> str:
        out = (" " * 4 * indent) + "Italics Node\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out

    def html(self: Self, external: bool) -> str:
        out = "<i>"
        for child in self.children:
            out += child.html(external)
        return out + "</i>"


@dataclass
class BoldNode(Node):
    children: list[Node]

    def dump(self: Self, indent: int) -> str:
        out = (" " * 4 * indent) + "Bold Node\n"
        for child in self.children:
            out += child.dump(indent + 1)
        return out

    def html(self: Self, external: bool) -> str:
        out = "<b>"
        for child in self.children:
            out += child.html(external)
        return out + "</b>"

# Leaf Nodes


@dataclass
class MediaNode(Node):
    type: str
    source: str
    text: str

    def __init__(self: Self, children: list[Node]):
        if len(children) == 1 and isinstance(children[0], TextNode):
            parts = children[0].text.split("](")
            if len(parts) == 2:
                self.text = parts[0]
                self.source = parts[1]
                extension = splitext(self.source)[1]
                if extension == ".png" or extension == ".jpg":
                    self.type = "image"
                elif extension == ".mp4" or extension == ".webm":
                    self.type = "video"

    def dump(self: Self, indent: int) -> str:
        return (" " * 4 * indent) + f"""Media Node:
            {self.type} - {self.source} - {self.text}\n"""

    def html(self: Self, external: bool) -> str:
        base_path = _media_base_path
        if external:
            base_path = _external_media_base_path
        if self.type == "image":
            out = f"<img src=\"{base_path + self.source}\" alt=\"{self.text}\"></img>"
        elif self.type == "video":
            out = f"""<video controls>
            <source src=\"{base_path + self.source}\"/>
            Video tag unsupported!</video>"""
        if self.text != "":
            out += f"<label class=\"media-caption\">{self.text}</label>"
        return out


@dataclass
class LinkNode(Node):
    source: str
    text: str

    def __init__(self: Self, children: list[Node]):
        if len(children) == 1 and isinstance(children[0], TextNode):
            parts = children[0].text.split("](")
            if len(parts) == 2:
                self.text = parts[0]
                self.source = parts[1]

    def dump(self: Self, indent: int) -> str:
        return (" " * 4 * indent) + f"Link Node: {self.source}, {self.text}\n"

    def html(self: Self, external: bool) -> str:
        return f"<a href=\"{self.source}\">{self.text}</a>"


@dataclass
class TextNode:
    text: str

    def dump(self: Self, indent: int) -> str:
        return (" " * 4 * indent) + "Text Node: \"" + self.text + "\"\n"

    def html(self: Self, external: bool) -> str:
        return self.text
