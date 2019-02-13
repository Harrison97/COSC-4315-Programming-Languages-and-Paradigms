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

class Token:
    def __init__(self, loc, kind):
        self.loc = loc
        self.kind = kind

    def __str__(self):
        return str(self.kind)

class Lexer:
    def __init__(self, text):
        self.text = text
        self.line = 1
        self.col = 1

    def tokenize(self):
        current_match = None

        #location list to store each tokens location
        loc = []
        kind = []

        #for loop does basic lexical analysis on the input and adds to the lists
        #returns a  Token(loc[], kind[])
        for index, c in enumerate(self.text):
            if c.isalpha():
                kind.append(TokenKind.ID)
            elif c == '(':
                kind.append(TokenKind.LPAR)
            elif c == ')':
                kind.append(TokenKind.RPAR)
            elif c == '!':
                kind.append(TokenKind.NOT)
            elif c == '/':
                if self.text[index + 1] == '\\':
                    kind.append(TokenKind.AND)
            elif c == '\\':
                if self.text[index + 1] == '/':
                    kind.append(TokenKind.OR)
            elif c == '=':
                if self.text[index + 1] == '>':
                    if self.text[index - 1] != '<':
                            kind.append(TokenKind.IMPLIES)
            elif c == '<':
                if self.text[index + 1] == '=':
                    if self.text[index + 2] == '>':
                        kind.append(TokenKind.IFF)
            elif c == ',':
                kind.append(TokenKind.COMMA)
            loc.append(Location(self.line, index + 1))

        return Token(loc, kind)
