from pysmt.shortcuts import Symbol, is_sat, Or

B = Symbol('B')
C = Symbol('C')

prop1 = Or(B, Xor(, C))

print prop1