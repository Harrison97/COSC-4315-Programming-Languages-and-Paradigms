from pysmt.shortcuts import Symbol, And, Not, is_sat, Iff


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
            if kind == 'ID':
                self.variables.append(self.value[index])
            elif kind == 'NOT':
                self.imports.append('NOT')
            elif kind == 'AND':
                self.imports.append('AND')
            elif kind == 'OR':
                self.imports.append('OR')
            elif kind == 'IMPLIES':
                self.imports.append('IMPLIES')
            elif kind == 'IFF':
                self.imports.append('IFF')

        print '\n'
        print self.imports
        print self.variables
        print '\n'

        f = open('test.py', 'w+')
        f.write('from pysmt.shortcuts import Symbol, is_sat')
        for imp in self.imports:
            f.write(', ' + imp)
        f.write('\n\n')

        for var in self.variables:
            f.write(var + ' = Symbol(\'' + var + '\')\n')
