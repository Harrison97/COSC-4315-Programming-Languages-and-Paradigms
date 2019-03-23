import string
UPPER_CASE = set(string.ascii_uppercase)

class Location:
    def __init__(self, line, col):
        self.col = col
        self.line = line

class TokenKind:
    ID = 'ID'   # identifier
    LPAR ='LPAR' # (
    RPAR = 'RPAR' # )
    NOT = 'NOT'  # !
    AND = 'AND'  # /\
    OR = 'OR'   # \/
    IMPLIES = 'IMPLIES'  # =>
    IFF = 'IFF'  # <=>
    COMMA = 'comma' # ,
    XOR = 'XOR' # \./

class Token:
    def __init__(self, loc, kind, value):
        self.loc = loc
        self.kind = kind
        self.value = value

    def __str__(self):
        return str(self.kind)

class Lexer:
    def __init__(self, text):
        self.text = text
        self.line = 1
        self.col = 1

    def tokenize(self):
        #current_match = None

        #location list to store each tokens location
        loc = []
        kind = []
        value = []

        #for loop does basic lexical analysis on the input and adds to
        #the lists, along with the actual value
        #returns a  Token(loc[], kind[])
        for index, c in enumerate(self.text):
            if c.isalpha():
                kind.append(TokenKind.ID)
                value.append(c)
            elif c == '(':
                kind.append(TokenKind.LPAR)
                value.append(c)
            elif c == ')':
                kind.append(TokenKind.RPAR)
                value.append(c)
            elif c == '!':
                kind.append(TokenKind.NOT)
                value.append(c)
            elif c == '/':
                if self.text[index + 1] == '\\':
                    kind.append(TokenKind.AND)
                    value.append(c)
            elif c == '\\':
                if self.text[index + 1] == '/':
                    kind.append(TokenKind.OR)
                    value.append(c)
                elif self.text[index + 1] == '.':
                    if self.text[index + 2] == '/':
                        kind.append(TokenKind.XOR)
                        value.append(c)
            elif c == '=':
                if self.text[index + 1] == '>':
                    if self.text[index - 1] != '<':
                            kind.append(TokenKind.IMPLIES)
                            value.append(c)
            elif c == '<':
                if self.text[index + 1] == '=':
                    if self.text[index + 2] == '>':
                        kind.append(TokenKind.IFF)
                        value.append(c)
            elif c == ',':
                kind.append(TokenKind.COMMA)
                value.append(c)
            loc.append(Location(self.line, index + 1))

        return Token(loc, kind, value)
