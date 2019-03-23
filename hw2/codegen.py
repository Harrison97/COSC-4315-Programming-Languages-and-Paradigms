from pysmt.shortcuts import Symbol, And, Not, is_sat, Iff
from lexer import TokenKind
import subprocess

class CodeGen:
    def __init__(self, tokelist, parseTree):
        self.kind = tokelist.kind
        self.value = tokelist.value
        self.parseTree = parseTree
        self.imports = []
        self.variables = []
        self.generated = False

    def generate(self):
        # If the parseTree returns an Error, Do not generate Code.
        if self.parseTree[:12] == 'Syntax Error':
            return 'Code not generated because of Syntax Error'

        # for loop goes through tokelist and builds a list for
        # variables needed and a list for imports needed
        for index, kind in enumerate(self.kind):
            if (kind == TokenKind.ID
                    and self.value[index] not in self.variables):

                self.variables.append(self.value[index])

            elif (kind == TokenKind.NOT
                    or kind == TokenKind.AND
                    or kind == TokenKind.OR
                    or kind == TokenKind.IMPLIES
                    or kind == TokenKind.IFF
                    or kind == TokenKind.XOR):

                if kind[0] + kind[1:].lower() not in self.imports:
                    self.imports.append(kind[0] + kind[1:].lower())

            elif kind == TokenKind.COMMA and 'And' not in self.imports:
                self.imports.append('And')

        # write the imports
        f = open('output.py', 'w+')
        f.write('from pysmt.shortcuts import Symbol, is_sat')
        for imp in self.imports:
            f.write(', ' + imp)
        f.write('\n\n')

        # write the variables
        for var in self.variables:
            f.write(var + ' = Symbol(\'' + var + '\')\n')
        f.write('\n')


        # build the list of propositions separated by commas
        props = []
        variable = ''
        proposition = ''
        action = ''
        for index, node in reversed(list(enumerate(self.parseTree))):
            if node is 'propositions':
                props.append(proposition)
            elif node == TokenKind.ID:
                variable = self.value.pop()
            # set action if needed
            elif (node == TokenKind.NOT
                    or node == TokenKind.AND
                    or node == TokenKind.OR
                    or node == TokenKind.IMPLIES
                    or node == TokenKind.IFF
                    or node == TokenKind.XOR
                    ##### sets action to something so that the
                    ##### else block below still works
                    or node == TokenKind.LPAR):
                action = node
                self.value.pop()
            # pop and skip RPAR
            elif node == TokenKind.RPAR:
                self.value.pop()
            # reset vars for new proposition
            elif node == 'comma':
                proposition = ''
                variable = ''
                action= ''
                self.value.pop()
            # set or update the proposition
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
                elif action == TokenKind.RPAR:
                    pass
                elif action == TokenKind.LPAR:
                    pass
                else:
                    proposition = variable
                variable = ''
                action = ''
            else:
                pass

        # write props to output file
        for index, p in enumerate(reversed(list(props))):
            f.write('prop' + str(index + 1) + ' = ' + p + '\n')

        f.write('\n')

        # writes the print statement to output file
        if len(props) > 1:
            f.write('print is_sat(')
            for i in range(len(props) - 1):
                f.write('And(')
            for p in range(len(props)):
                f.write('prop' + str(p+1))
                if p == 0:
                    f.write(', ')
                elif p < len(props) - 1:
                    f.write('), ')
            f.write('))')
        else:
            f.write('print is_sat(prop1)')

        f.close()
        self.generated = True
        return 'Code Generated'


    def runCode(self):
        if self.generated:
            return subprocess.check_output(['python2', 'output.py'])[:-1]
        return self.parseTree

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

