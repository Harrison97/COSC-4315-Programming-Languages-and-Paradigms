import string
UPPER_CASE = set(string.ascii_uppercase)

class Location:
    def __init__(self, line, col):
        self.col = col
        self.line = line


class TokenKind:
    ID = 0   # identifier
    LPAR = 1 # (
    RPAR = 2 # )
    NOT = 3  # !
    AND = 4  # /\
    OR = 5   # \/
    IMPLIES = 6  # =>
    IFF = 7  # <=>
    COMMA = 8 # ,



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

        # the following assignment and if statement are only to allow the test pass. they need to be removed
        # c = self.text[0]
        # if c == 'Q':
            # return Token(Location(1, 1), [TokenKind.ID])

        loc = []
        kind = []
        for index, c in enumerate(self.text):
            if c.isalpha():
                kind.append(TokenKind.ID)
                loc.append(Location(1, index))
            elif c == '(':
                kind.append(TokenKind.LPAR)
                loc.append(Location(1, index))
            elif c == ')':
                kind.append(TokenKind.RPAR)
                loc.append(Location(1, index))
            elif c == '!':
                kind.append(TokenKind.NOT)
                loc.append(Location(1, index))
            elif c == '/':
                if self.text[index + 1] == '\\':
                    kind.append(TokenKind.AND)
                    loc.append(Location(1, index))
            elif c == '\\':
                if self.text[index + 1] == '/':
                    kind.append(TokenKind.OR)
                    loc.append(Location(1, index))
            elif c == '=':
                if self.text[index + 1] == '>':
                    if self.text[index - 1] != '<':
                            kind.append(TokenKind.IMPLIES)
                            loc.append(Location(1, index))
            elif c == '<':
                if self.text[index + 1] == '=':
                    if self.text[index + 2] == '>':
                        kind.append(TokenKind.IFF)
                        loc.append(Location(1, index))
            elif c == ',':
                kind.append(TokenKind.COMMA)
                loc.append(Location(1, index))
            # raise NotImplementedError

        return Token(loc, kind)