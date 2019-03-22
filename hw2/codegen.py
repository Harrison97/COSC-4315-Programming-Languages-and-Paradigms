from pysmt.shortcuts import Symbol, And, Not, is_sat, Iff
from lexer import TokenKind

#P /\ !Q

#P = Symbol("P") # Default type is Boolean
#
#Q = Symbol("Q")
#
#f = And(P, Not(Q))
#
#print is_sat(f)
#
#
#
##P /\ !Q, !P<=>!Q
#
#P = Symbol("P") # Default type is Boolean
#
#Q = Symbol("Q")
#
#prop1 = And(P, Not(Q))
#
#prop2 = Iff(Not(P),Not(Q))
#
#f = And(prop1, prop2)
#
#print is_sat(f)
#
#
#P = Symbol("P")
#Q = Symbol("Q")
#
#f = Iff(P, Q)
#
#print is_sat(f)

class CodeGen:
    def __init__(self, tokelist, parseTree):
        self.kind = tokelist.kind
        self.value = tokelist.value
        self.parseTree = parseTree
        self.imports = []
        self.variables = []

    def generate(self):
        for index, kind in enumerate(self.kind):
            if kind == TokenKind.ID and self.value[index] not in self.variables:
                self.variables.append(self.value[index])
            elif kind == TokenKind.NOT or kind == TokenKind.AND or kind == TokenKind.OR or kind == TokenKind.IMPLIES or kind == TokenKind.IFF:
                if kind[0] + kind[1:].lower() not in self.imports:
                    self.imports.append(kind[0] + kind[1:].lower())

        print '\n'
        print self.imports
        print self.variables
        print self.value
        print '\n'

        f = open('test.py', 'w+')
        f.write('from pysmt.shortcuts import Symbol, is_sat')
        for imp in self.imports:
            f.write(', ' + imp)
        f.write('\n\n')

        for var in self.variables:
            f.write(var + ' = Symbol(\'' + var + '\')\n')
        f.write('\n')

        #create a list for props and rebuild variables to have all instances on a var
        props = []
        #self.variables = []
        #for v in self.value:
        #    if v.isalpha():
        #        self.variables.append(v)

        print self.variables

        variable = ''
        proposition = ''
        action = ''
        parenthesis = ''
        #isNot = False
        #props.append('prop' + str(len(props)) + ' =  ')
        for index, node in reversed(list(enumerate(self.parseTree))):
            if node is 'propositions':
                props.append(proposition)
            if node == TokenKind.ID:
                variable = self.value.pop()
                #print variable
            elif node == TokenKind.NOT:
                action = TokenKind.NOT
                self.value.pop()
            elif node == TokenKind.AND:
                action = TokenKind.AND
                self.value.pop()
            elif node == TokenKind.OR:
                action = TokenKind.OR
                self.value.pop()
            elif node == TokenKind.IMPLIES:
                action = TokenKind.IMPLIES
                self.value.pop()
            elif node == TokenKind.IFF:
                action = TokenKind.IFF
                self.value.pop()
            elif node == TokenKind.XOR:
                action = TokenKind.XOR
                self.value.pop()
            elif node == TokenKind.RPAR:
                action = 'parentheses'
                self.value.pop()
            elif node == TokenKind.LPAR:
                action = TokenKind.XOR
                self.value.pop()
            elif node == 'comma':
                proposition = ''
                variable = ''
                action= ''
                self.value.pop()
            elif node == 'proposition':
                if action == TokenKind.NOT:
                    proposition = self.isNot(proposition)
                elif action == TokenKind.AND:
                    proposition = self.isAnd(variable, proposition)
                elif action == TokenKind.OR:
                    proposition = self.isOr(variable, proposition)
                elif action == TokenKind.IMPLIES:
                    proposition = self.isImplies(variable, proposition)
                elif action == TokenKind.IFF:
                    proposition = self.isIff(variable, proposition)
                elif action == TokenKind.XOR:
                    proposition = self.isXor(variable, proposition)
                else:
                    proposition = variable
                variable = ''
                action = ''
            else:
                pass
#            elif node == TokenKind.AND or TokenKind.OR or TokenKind.IMPLIES or TokenKind.IFF or TokenKind.XOR:
#                proposition = self.isNot(proposition)
#            elif node == TokenKind.OR:
#                proposition = self.isNot(proposition)
#            elif node == TokenKind.IMPLIES:
#                proposition = self.isNot(proposition)
#            elif node == TokenKind.IFF:
#                proposition = self.isNot(proposition)
#            elif node == TokenKind.XOR:
#                proposition = self.isNot(proposition)

        for index, p in enumerate(reversed(list(props))):
            f.write('prop' + str(index + 1) + ' = ' + p + '\n')

        f.write('\n')

        if len(props) > 1:
            f.write('print ')
            for i in range(len(props) - 1):
                f.write('And(')
            for p in range(len(props)):
                f.write('prop' + str(p+1))
                if p == 0:
                    f.write(', ')
                elif p < len(props) - 1:
                    f.write('), ')
            f.write(')')
        else:
            f.write('print prop1')



    def isNot(self, p):
        return 'Not(' + p + ')'

    def isAnd(self, v, p):
        return 'And(' + v + ', ' + p + ')'

    def isOr(self, v, p):
        return 'Or(' + v + ', ' + p + ')'

    def isImplies(self, v, p):
        return 'Implies(' + v + ', ' + p + ')'

    def isIff(self, v, p):
        return 'Iff(' + v + ', ' + p + ')'

    def isXor(self, v, p):
        return 'Xor(' + v + ', ' + p + ')'



