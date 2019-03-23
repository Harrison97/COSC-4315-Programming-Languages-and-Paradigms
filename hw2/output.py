from pysmt.shortcuts import Symbol, is_sat, Xor

Q = Symbol('Q')
P = Symbol('P')

prop1 = Xor(Q, P)

print is_sat(prop1)