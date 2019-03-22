from pysmt.shortcuts import Symbol, is_sat, And, Not, Iff

P = Symbol('P')
Q = Symbol('Q')

prop1 = And(P, Not(Q))
prop2 = Iff(Not(P), Not(Q))

props = And(prop1, prop2)

print is_sat(props)
