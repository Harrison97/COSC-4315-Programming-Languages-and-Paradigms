from pysmt.shortcuts import Symbol, is_sat, Or, And, Implies

P = Symbol('P')
Q = Symbol('Q')
X = Symbol('X')
Y = Symbol('Y')

prop1 = Or(P, Q)
prop2 = Implies(X, Y)

print is_sat(And(prop1, prop2))