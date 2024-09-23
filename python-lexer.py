import dataclasses
import typing as t

CHAR_EOF = None
ERROR = "ERROR"  # enum
XML_EXAMPLE = """\
<article>
    <author>John</author>
    <id>12</id>
    <title>My title</title>
    <sec><p>Paragraph 1</p>
        <p>Paragraph 2</p>
    </sec>
</article>
"""


@dataclasses.dataclass
class Lexer:
    input: str  # scanned string
    # Note that only when you emit or ignore
    # you move the lexer.start counter to lexer.pos
    start: int  # start of lexeme
    pos: int  # possible end of lexeme
    tokens: t.Any

    def __str__(self):
        return f"Lexer(start={self.start}, pos={self.pos}, tokens={self.tokens})"


@dataclasses.dataclass
class Token:
    kind: str
    lexeme: str


def lexer(_input: str):
    print(">> lexer")
    temp_queue = []  # TODO: replace with real queue
    return Lexer(_input, 1, 0, temp_queue)


def lexeme(l: Lexer) -> None:
    print(">> lexeme")
    stop = l.pos - 1
    l.input[l.start : stop]


def lex(_input: str, start: t.Callable) -> Lexer:
    print(">> lex")
    l = lexer(_input)
    run(l, start)
    return l


def run(lexer: Lexer, start: t.Callable):
    print(">> run")
    state = start
    while state.__name__ != lex_end.__name__:
        try:
            state = state(lexer)
        except:
            print("lexer", lexer)
            raise
    print("run ended")


def emit_token(l: Lexer, token: str) -> t.Callable:
    print(f">> emit_token, token={token}")
    l.tokens.append(token)
    l.start = l.pos


def lex_xml(l: Lexer) -> t.Callable:
    print(">> lex_xml")
    while True:
        ignore_whitespace(l)
        ch = peek_char(l)
        # TODO: in go here check EOF char
        if ch is CHAR_EOF:
            emit_token(l, CHAR_EOF)
            return lex_end
        elif ch == "<":
            # TODO: improve peek next next char
            if len(l.input) > l.pos and l.input[l.pos + 1] == "/":
                l.pos += len("</")
                emit_token(l, "</")
                return lex_inside_end_tag
            l.pos += len("<")
            emit_token(l, "<")
            return lex_inside_start_tag
        elif ch.isalnum():
            return lex_text
        else:
            raise Exception(f"Found unexpected character {ch}.")
            # error(l, f"Found unexpected character {ch}.")


def lex_text(l: Lexer) -> t.Callable:
    print(">> lex_text")
    ch = peek_char(l)
    while ch not in ["<", ">", CHAR_EOF]:
        next_char(l)
        ch = peek_char(l)
    token = l.input[l.start : l.pos]
    emit_token(l, token)
    return lex_xml


def lex_inside_start_tag(l: Lexer) -> t.Callable:
    print(">> lex_inside_start_tag")
    ch = peek_char(l)
    while ch != ">":
        next_char(l)
        ch = peek_char(l)
    token = l.input[l.start : l.pos]
    emit_token(l, token)
    closing_brachet = next_char(l)  # >
    emit_token(l, closing_brachet)
    return lex_xml


def lex_inside_end_tag(l: Lexer) -> t.Callable:
    # TODO: similar to inside_start_tag but without attribs, namespaces, etc
    return lex_inside_start_tag(l)


def lex_end_tag(l: Lexer) -> t.Callable:
    return lex_xml


def lex_end(_: Lexer) -> t.Callable:
    print(">> lex_end")
    return lex_end


def ignore_whitespace(l: Lexer):
    print(">> ignore_whitespace")
    while peek_char(l).isspace():
        next_char(l)
    l.start = l.pos


def backup_char(l: Lexer) -> str:
    # TODO: is this necessary?
    print(">> backup_char")
    l.pos -= 1
    return l.input[l.pos]


def peek_char(l: Lexer) -> str:
    print(">> peek_char")
    if l.pos > len(l.input):
        return CHAR_EOF
    return l.input[l.pos]


def next_char(l: Lexer) -> str:
    print(">> next_char")
    if l.pos > len(l.input):
        return CHAR_EOF
    ch = l.input[l.pos]
    l.pos += 1
    return ch


def next_token(l: Lexer) -> str:
    print(">> next_token")
    return l.tokens.pop()


def ignore(l: Lexer) -> None:
    print(">> ignore")
    l.start = l.pos


def error(l: Lexer, msg: str) -> t.Callable:
    print(">> error")
    token = Token(kind=ERROR, lexeme=msg)
    token = msg
    l.tokens.append(token)
    return lex_end


if __name__ == "__main__":
    lex(XML_EXAMPLE, lex_xml)
