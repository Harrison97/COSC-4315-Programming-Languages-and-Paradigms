# -- Evaluating Expressions in Haskell --

## Programming Languages and Paradigms

>Harrison Hayes

>4/2/2019

>Amin Alipour

>COSC 4315

**Haskell ghci Version 8.6.4**

## To Open ghci and load the File:

    $ghci main.hs
    $ghci :load main.hs

## To Run Built in Tests:

    >eval a // -(-(10))     = 10
    >eval b // -(10)        = -10
    >eval c // (2+3)+(2-1)  = 4
    >eval d // (10^2)*(2^3) = 800

## To Write and Evaluate Your Own Expression 

### Defined Semantics of Binary Operators

binsemantic Add  = (+)

binsemantic Sub  = (-)

binsemantic Mult  = (*)

binsemantic Pow  = (^)

### Defined Semantics of Unary Operators

unisemantic Neg  = (*(-1))

unisemantic Inc  = (+1)

    >eval (<UniExp | BinExp> <operator> <expression | (Val <value>)>)

### Example:

    >eval (UniExp Neg (Val 10))
    >-10
    >eval (BinExp Mult (BinExp Pow (Val 10) (Val 2)) (BinExp Pow (Val 2) (Val 3)))
    >800
