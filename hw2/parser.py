from lexer import TokenKind, Location, Lexer
import sys, warnings

class VariableType:
    PROPOSITIONS = 0
    PROPOSITION  = 1
    ATOMIC       = 2
    MOREPROPOSITIONS = 3
    COMPOUND = 4
    CONNECTIVE = 5

class Parser:
    def __init__(self):
        #self.loc = Location(0, 0)
        self.parseTree = []
        self.current = None
        self.next = None
        self.tokens = []
        self.loc = []

    #initial function to call
    def parse(self, tokenList):
        self.tokens = tokenList.kind
        self.loc = tokenList.loc
        self.current = 0
        if len(self.tokens) > 1:
            self.next = 1

        #tries to run it through the parser, starting w props
        try:
            self.propositions()
        #takes syntax errors from other functions and throws a custom
        #Syntax Error with the location of the error
        except Exception:
            #pass
            #raise SyntaxError(str('Syntax Error at line ' + str(self.loc[self.current].line)
            #        + ' column ' + str(self.loc[self.current].col) + '.'))
            print self.parseTree
            return str('Syntax Error at line ' + str(self.loc[self.current].line)
                    + ' column ' + str(self.loc[self.current].col) + '.')
        return self.parseTree

    # match function consumes the token if is is the tried token
    # then iterates to next tokens
    def match(self, token):
        if self.tokens[self.current] == token:
            if len(self.tokens) > self.current + 1:
                self.current += 1
            else:
                self.current = None
            if self.next != None and len(self.tokens) > self.next + 1:
                self.next += 1
            else:
                self.next = None
        pass

    def propositions(self): # -> proposition more-ropositions
        self.parseTree.append('propositions')
        self.proposition()
        self.more_propositions()

    def more_propositions(self): # -> , propositions | epsilon
        self.parseTree.append("more-proposition")
        #print self.tokens[self.current]
        #print self.tokens[self.current] == TokenKind.COMMA
        if self.current == None:
            self.parseTree.append('epsilon')
            return True
        elif self.isToken(TokenKind.COMMA):
            self.propositions()
            return True
        raise Exception
        return False

    def proposition(self): # -> atomic | compound
        self.parseTree.append("proposition")

        if self.atomic():
            return True
        elif self.compound():
            return True
        return False

    def atomic(self): # -> 0 | 1 | ID (All go to ID)
        #print self.current
        #print self.next
        if self.isToken(TokenKind.ID):
            return True
        return False

    def compound(self): # -> atomic connective proposition | LPAR proposition RPAR | NOT proposition
        self.parseTree.append("compound")
        if self.atomic() and self.connective() and self.proposition():
            return True
        elif self.isToken(TokenKind.LPAR) and self.proposition() and self.isToken(TokenKind.RPAR):
            return True
        elif self.isToken(TokenKind.NOT) and self.proposition():
            return True
        raise Exception
        return False

    def connective(self): # -> AND | OR | IMPLIES | IFF
        self.parseTree.append("connective")
        if self.isToken(TokenKind.AND):
            return True
        if self.isToken(TokenKind.OR):
            return True
        if self.isToken(TokenKind.IMPLIES):
            return True
        if self.isToken(TokenKind.IFF):
            return True
        if self.isToken(TokenKind.XOR):
            return True
        return False

    # checks to see if the current token is the tried token
    # appends to the tree
    # matches the token
    def isToken(self, token):
        if self.tokens[self.current] == token:
            if token == TokenKind.ID:
                if self.next == None:
                    pass
                elif sys._getframe(2).f_code.co_name == 'compound':
                    pass
                elif self.tokens[self.next] == TokenKind.RPAR:
                    pass
                else:
                    return False
                self.parseTree.append('atomic')
            self.parseTree.append(token)
            self.match(token)
            return True
        return False

