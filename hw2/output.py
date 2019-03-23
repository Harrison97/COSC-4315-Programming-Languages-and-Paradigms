from pysmt.shortcuts import Symbol, is_sat, And, Or

A = Symbol('A')
B = Symbol('B')
C = Symbol('C')
D = Symbol('D')

prop1 = And(A, And(B, Or(C, D)))
prop2 = Or(A, C)

print is_sat(And(prop1, prop2))