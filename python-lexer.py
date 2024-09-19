import dataclasses
import typing as t

CHAR_EOF = None
ERROR = "ERROR" # enum
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
    input: str # scanned string
    start: int # start of lexeme
    pos: int # possible end of lexeme
    tokens: t.Any

    def __str__(self):
        return f"Lexer(start={self.start}, pos={self.pos}, tokens={self.tokens})"

@dataclasses.dataclass
class Token:
    kind: str
    lexeme: str

def lexer(_input: str):
    temp_queue = [] # TODO: replace with real queue
    return Lexer(_input, 1, 0, temp_queue)

def lexeme(l: Lexer) -> None:
	stop = l.pos - 1
	l.input[l.start:stop]

def lex(_input: str, start: t.Callable) -> Lexer:
    l = lexer(_input)
    run(l, start)
    return l

def run(lexer: Lexer, start: t.Callable):
    state = start
    print("run() runs", state.__name__)
    while state.__name__ != lex_end.__name__:
        print("state.__name__", state.__name__)
        state = state(lexer)
        print("state", state)
    print("run ended")

def emit_token(lexer: Lexer, token: str) -> t.Callable:
    lexer.tokens.append(token)
    lexer.start = lexer.pos

def lex_xml(l: Lexer) -> t.Callable:
    while True:
        ignore_whitespace(l)
        ch = peek_char(l)
        print("lex_xml.ch", ch)
        print("l", l)
        if ch is CHAR_EOF:
            emit_token(l, CHAR_EOF)
            return lex_end
        elif ch == "<":
            emit_token(l, "<")
            return lex_begin_tag
        else:
            return lex_text

def lex_text(l: Lexer) -> t.Callable:
    ch = peek_char(l)
    print("lex_text.1.ch", ch)
    while ch not in ["<", ">", CHAR_EOF]:
        next_char(l)
        ch = peek_char(l)
        print("lex_text.2.ch", ch)
    print("l.start", l.start, "l.pos", l.pos)
    print("l.input[1:l.pos]", l.input[1:l.pos])
    print("l.input[l.start:l.pos]", l.input[l.start:l.pos])
    token = l.input[l.start:l.pos]
    print("l", l)
    emit_token(l, token)
    print(">> token", token)
    raise NotImplementedError
    return lex_xml 

def lex_begin_tag(l: Lexer) -> t.Callable:
    print("lexer", l)
    ch = peek_char(l)
    print("lex_begin_tag.ch", ch)
    if ch == "/":
        print("CLOSE TAG")
    else:
        print("inside tag")
        return lex_inside_tag

def lex_inside_tag(l: Lexer) -> t.Callable:
    ch = next_char(l)
    print("lex_inside_tag.ch", ch)
    print("lexer", lexer)
    # TODO: verify inside tag


    print("l.pos before update", l.pos)
    pos = l.input.find(">", l.pos)
    if pos == -1:
        return error(l, "Found unclosed tag")
    l.pos = pos
    print("l.pos after update", l.pos)



    raise Exception("Here is the problem - why is the l.start at 0 and not at 1???")

    print("lexer", l)
    print(">> l.input[l.start:l.pos]", l.input[l.start:l.pos])
    emit_token(l, l.input[l.start:l.pos])
    # handle attributes
    # handle closing a tag
    return lex_xml

def lex_end(_: Lexer) -> t.Callable:
    return lex_end

def ignore_whitespace(l: Lexer):
    while peek_char(l).isspace():
        next_char(l)
    print("ignore_whitespace".upper())
    l.start = l.pos

def backup_char(l: Lexer) -> str:
	l.pos -= 1
	return l.input[l.pos]

def peek_char(l: Lexer) -> str:
    if l.pos > len(l.input):
        return CHAR_EOF
    return l.input[l.pos]

def next_char(l: Lexer) -> str:
    if l.pos > len(l.input):
        return CHAR_EOF
    ch = l.input[l.pos]
    l.pos += 1
    return ch

def next_token(l: Lexer) -> str:
    return l.tokens.pop()

def ignore(l: Lexer) -> None:
    l.start = l.pos

def error(l: Lexer, msg: str) -> t.Callable:
    token = Token(kind=ERROR, lexeme=msg)
    l.tokens.append(token)
    return lex_end


if __name__ == "__main__":
    lex(XML_EXAMPLE, lex_xml)
