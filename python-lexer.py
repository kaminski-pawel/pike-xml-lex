import dataclasses
import typing as t

CHAR_EOF = None
XML_EXAMPLE = """
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

    # def __str__(self):
        # return self.input[self.start, self.pos] 

@dataclasses.dataclass
class Token:
    kind: str
    lexeme: str

def lexer(_input: str):
    temp_queue = [] # TODO: replace with real queue
    return Lexer(_input, 1, 0, temp_queue)

def lex_end(lexer): 
    return lex_end

def lex(_input: str, start: t.Callable):
    l = lexer(_input)
    run(l, start)
    return l

def run(lexer, start: t.Callable):
    state = start
    print("run() runs", state.__name__)
    while state.__name__ != lex_end.__name__:
        print("state.__name__", state.__name__)
        state = state(lexer)
        print("state", state)
    print("run ended")

def emit_token(lexer, char):
    print(char)

def lex_xml(lexer):
    while True:
        ignore_whitespace(lexer)
        ch = peek_char(lexer)
        print("lex_xml.ch", ch)
        if ch is CHAR_EOF:
            emit_token(lexer, CHAR_EOF)
            return lex_end
        elif ch == "<":
            return lex_begin_tag
        else:
            return lex_text

def lex_text(lexer):
    ch = peek_char(lexer)
    print("lex_text.1.ch", ch)
    while ch not in ["<", ">", CHAR_EOF]:
        next_char(lexer)
        ch = peek_char(lexer)
        print("lex_text.2.ch", ch)
    token = lexer.input[lexer.start:lexer.pos]
    emit_token(lexer, token) 
    print(token, "token")
    raise NotImplementedError
    return lex_xml 

def lex_begin_tag(lexer):
    print("lexer", lexer)
    ch = peek_char(lexer)
    print("lex_begin_tag.ch", ch)
    if ch == "/":
        print("CLOSE TAG")
    else:
        print("inside tag")
        return lex_inside_tag

def lex_inside_tag(l):
    ch = next_char(l)
    print("lex_inside_tag.ch", ch)
    # TODO: verify inside tag
    pos = l.input.find(">", l.pos)
    if pos == -1:
        return error(l, "Found unclosed tag")
    l.pos = pos
    emit_token(l, "INSIDE_TAG")
    ...
    return lex_xml

def ignore_whitespace(lexer):
    while peek_char(lexer).isspace():
        next_char(lexer)
    lexer.start = lexer.pos

def peek_char(lexer):
    if lexer.pos > len(lexer.input):
        return CHAR_EOF
    return lexer.input[lexer.pos]

def next_char(lexer):
    if lexer.pos > len(lexer.input):
        return CHAR_EOF
    # ch, lexer.pos = next(lexer.input, lexer.pos)
    # is this similar to?:
    ch = lexer.input[lexer.pos]
    lexer.pos += 1
    return ch

def next_token(lexer):
    return lexer.tokens.pop()


if __name__ == "__main__":
    lex(XML_EXAMPLE, lex_xml)

