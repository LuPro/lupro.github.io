from typing import Self, Callable
from mdparsertypes import (
    Node,
    Tree,
    HeaderNode,
    ParagraphNode,
    ListBlockNode,
    ListElementNode,
    StrikethroughNode,
    ItalicsNode,
    BoldNode,
    TextNode,
    InlineCodeNode,
    CodeBlockNode,
    LinkNode,
    MediaNode
)


class MarkdownParser:
    _index: int
    _data: str

    _stop_on_single_newline: bool = False
    _inside_code_block: bool = False

    _inside_flags: dict = {
        "italics": False,
        "bold": False,
        "strikethrough": False,
        "inline_code": False,
        "quote": False,
        "link": False,
        "media": False
    }

    def parse(self: Self, data: str):
        self._data = data
        self._index = 0

        nodes = self._parse_blocks()

        return Tree(nodes)

    def _parse_blocks(self: Self) -> list[Node]:
        children: list[Node] = []

        while not self._is_eof():
            self._reset_flags()

            header_level = self._determine_header_level()
            list_level = self._determine_list_indent_level()
            if header_level > 0:
                self._consume(header_level + 1)
                children.append(self._parse_header(header_level))

            # TODO that check is ugly
            elif self._peek() == "`" and self._peek(1) == "`" and self._peek(2) == "`":
                children.append(self._parse_code_block())
            elif list_level > 0:
                children.append(self._parse_unordered_list(list_level))
            else:
                children.append(self._parse_paragraph())

        return children

    # Figures out header level, returns 0 if it's not a header
    def _determine_header_level(self: Self) -> int:
        level = 0
        while self._peek(level) == "#":
            level += 1

        if level > 6:
            # More header levels than 6 aren't supported
            return 0

        if self._peek(level) == " ":
            return level

        return 0

    def _determine_list_indent_level(self: Self) -> int:
        level = 0
        # TODO that check is ugly
        while self._peek(level) == " " and self._peek(level + 1) == " " and self._peek(level + 2) == " " and self._peek(level + 3) == " ":
            level += 1

        # Keep my insanity of nesting stuff in check
        if level > 3:
            return 0

        if self._peek(level * 4) == "-" and self._peek(level * 4 + 1) == " ":
            return level + 1
        return 0

    def _consume_list_indent(self: Self) -> None:
        while self._peek() == " ":
            self._consume()

        self._consume(2)

    def _parse_header(self: Self, level: int) -> HeaderNode:
        self._stop_on_single_newline = True
        children = self._parse_rich_text()
        self._stop_on_single_newline = False
        return HeaderNode(children, level)

    def _parse_paragraph(self: Self) -> ParagraphNode:
        children = self._parse_rich_text()
        return ParagraphNode(children)

    def _parse_code_block(self: Self) -> CodeBlockNode:
        self._inside_code_block = True
        self._consume(3)
        children = self._parse_rich_text()
        self._inside_code_block = False
        # TODO I don't actually want rich text in a code block
        return CodeBlockNode(children)

    def _parse_unordered_list(self: Self, list_level: int) -> ListBlockNode:
        self._consume_list_indent()
        self._stop_on_single_newline = True
        children = []
        while True:
            children.append(ListElementNode(self._parse_rich_text()))
            new_list_level = self._determine_list_indent_level()
            if new_list_level < list_level:
                break
            elif new_list_level > list_level:
                children.append(self._parse_unordered_list(new_list_level))
            self._consume_list_indent()
        return ListBlockNode(children)

    def _run_symmetric_content_rule(self: Self,
                                    rule: tuple[str, str, Callable],
                                    children: list[Node],
                                    start_index: int,
                                    end_index: int) -> (list[Node], int, bool):
        for n, char in enumerate(rule[1]):
            if char != self._peek(n):
                return (children, start_index, False)

        if self._inside_flags[rule[0]]:
            return (children, start_index, True)

        self._consume(len(rule[1]))
        children.append(TextNode(self._data[start_index:end_index]))
        children += self._parse_symmetric_rule(rule)
        return (children, self._index, False)

    def _run_asymmetric_content_rule(self: Self,
                                     rule: tuple[str, str, str, Callable],
                                     children: list[Node],
                                     start_index: int,
                                     end_index: int) -> (list[Node], int, bool):
        should_exit_start = False
        for n, char in enumerate(rule[1]):
            if char != self._peek(n):
                should_exit_start = True
                break

        should_exit_end = False
        if self._inside_flags[rule[0]]:
            for n, char in enumerate(rule[2]):
                if char != self._peek(n):
                    should_exit_end = True
                    break

            if not should_exit_end:
                return (children, start_index, True)

        if should_exit_start or should_exit_end:
            return (children, start_index, False)

        self._consume(len(rule[1]))
        children.append(TextNode(self._data[start_index:end_index]))
        children += self._parse_asymmetric_rule(rule)
        return (children, self._index, False)

    def _parse_rich_text(self: Self, in_recursion: bool = False) -> list[Node]:
        children: list[Node] = []

        start_index = self._index
        end_index = self._index
        while not self._is_eof():
            end_index = self._index

            # Rich content parsing

            # italics, bold and combination need to be handled specially due
            # to potential nesting
            if not self._inside_code_block:
                if self._peek() == "*":
                    # One asterisk -> italics

                    if self._peek(1) == "*":
                        # Two asterisks -> bold
                        # _parse_bold() handles triple asterisk for both
                        if self._inside_flags["bold"]:
                            break

                        self._consume(2)
                        children.append(
                            TextNode(self._data[start_index:end_index]))
                        children += self._parse_bold()
                        start_index = self._index

                    else:
                        if self._inside_flags["italics"]:
                            break

                        self._consume()
                        children.append(
                            TextNode(self._data[start_index:end_index]))
                        children += self._parse_symmetric_rule(
                            ("italics", "*", ItalicsNode))
                        start_index = self._index

                # regular rich content rules
                rules = [
                    ("inline_code", "`", InlineCodeNode),
                    ("strikethrough", "~~", StrikethroughNode),
                    ("link", "[", ")", LinkNode),
                    ("media", "![", ")", MediaNode)
                ]

                should_break = False
                for rule in rules:
                    if len(rule) == 3:
                        (children, start_index, should_break) = self._run_symmetric_content_rule(
                            rule, children, start_index, end_index)
                    if len(rule) == 4:
                        (children, start_index, should_break) = self._run_asymmetric_content_rule(
                            rule, children, start_index, end_index)
                    if should_break:
                        break

                if should_break:
                    break

            # Conditions for ending current block on newline
            if self._peek() == "\n":
                # We reached the end of line
                if self._inside_code_block:
                    if self._peek(1) == "`" and self._peek(2) == "`" and self._peek(3) == "`":
                        if not in_recursion:
                            self._consume(4)
                        break
                else:
                    if self._stop_on_single_newline:
                        if not in_recursion:
                            # If we're deeper in recursion we mustn't consume
                            # the line end, otherwise our start of recursion
                            # stack will not know the line ended and will blend
                            # lines together. Same as with the checks below
                            self._consume()
                        break

                    if self._peek(1) == "\n":
                        # It's a double newline -> new paragraph
                        if not in_recursion:
                            self._consume(2)
                        break

                    if self._peek(1) == "#":
                        # Next line starts with hash -> potential heading
                        if not in_recursion:
                            self._consume()
                        break
                    if self._peek(1) == "-":
                        # Next line starts with dash -> potential list
                        if not in_recursion:
                            self._consume()
                        break

            self._consume()

        if end_index > start_index:
            text = self._data[start_index:end_index]
            children.append(TextNode(text))
        return children

    def _parse_bold(self: Self) -> list[Node]:
        self._inside_flags["bold"] = True
        children: list[Node] = []
        if self._peek() == "*":
            # If there is a third asterisk, also add italics
            self._consume()
            children = self._parse_symmetric_rule(("italics", "*", ItalicsNode))

        children += self._parse_rich_text(True)

        if self._match("**"):
            self._inside_flags["bold"] = False
            return [BoldNode(children)]

        return [TextNode("**")] + children

    # regular content rule parser
    def _parse_symmetric_rule(self: Self, rule: tuple[str, str, Node]) -> list[Node]:
        self._inside_flags[rule[0]] = True
        children = self._parse_rich_text(True)

        if self._match(rule[1]):
            self._inside_flags[rule[0]] = False
            return [rule[2](children)]

        return [TextNode(rule[1])] + children

    def _parse_asymmetric_rule(self: Self, rule: tuple[str, str, str, Node]) -> list[Node]:
        self._inside_flags[rule[0]] = True
        children = self._parse_rich_text(True)

        # TODO I need matching here to check for "internal structure"
        # eg: links need exactly one "](" inside to be valid
        # I can't do the check in the node constructor otherwise
        # I can't properly insert incorrect syntax back into the HTML
        if self._match(rule[2]):
            self._inside_flags[rule[0]] = False
            return [rule[3](children)]

        return [TextNode(rule[1])] + children

    # helpers
    def _is_eof(self: Self) -> bool:
        return self._index >= len(self._data)

    def _consume(self: Self, n: int = 1) -> str:
        if self._is_eof():
            return "\0"

        out = self._data[self._index]
        if n > 1:
            end_index = self._index + n
            out = self._data[self._index:min(end_index, len(self._data) - 1)]
        self._index += n
        return out

    def _match(self: Self, matchStr: str) -> bool:
        for n, char in enumerate(matchStr):
            if char != self._peek(n):
                return False

        self._index += len(matchStr)
        return True

    def _peek(self: Self, n: int = 0) -> str:
        if self._index + n >= len(self._data):
            return '\0'

        return self._data[self._index + n]

    def _reset_flags(self: Self):
        self._stop_on_single_newline = False
        self._inside_code_block = False

        self._inside_flags["italics"] = False
        self._inside_flags["bold"] = False
        self._inside_flags["strikethrough"] = False
        self._inside_flags["inline_code"] = False
        self._inside_flags["quote"] = False
        self._inside_flags["link"] = False
        self._inside_flags["media"] = False
