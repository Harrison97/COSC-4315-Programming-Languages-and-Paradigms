import unittest
import sys
from lexer import Lexer, TokenKind
from parser import Parser
from codegen import CodeGen


class Test(unittest.TestCase):

    ########### lexer tests #########

    def test_lexer_1(self):
        l = Lexer('Q').tokenize()
        self.assertEqual(l.kind, [TokenKind.ID])

    def test_lexer_2(self):
        l = Lexer('!Q').tokenize()
        self.assertEqual(l.kind, [TokenKind.NOT, TokenKind.ID])

    def test_lexer_3(self):
        l = Lexer('P <=> Q').tokenize()
        self.assertEqual(l.kind, [TokenKind.ID, TokenKind.IFF, TokenKind.ID])

    def test_lexer_4(self):
        l = Lexer('( P /\ Q )').tokenize()
        self.assertEqual(l.kind, [TokenKind.LPAR, TokenKind.ID, TokenKind.AND,
            TokenKind.ID, TokenKind.RPAR])

    def test_lexer_5(self):
        l = Lexer('( P \/ Q ) , ( X => Y )').tokenize()
        self.assertEqual(l.kind, [TokenKind.LPAR, TokenKind.ID, TokenKind.OR,
            TokenKind.ID, TokenKind.RPAR, TokenKind.COMMA, TokenKind.LPAR,
            TokenKind.ID, TokenKind.IMPLIES, TokenKind.ID, TokenKind.RPAR])

    def test_lexer_6(self):
        l = Lexer(')Q').tokenize()
        self.assertEqual(l.kind, [TokenKind.RPAR, TokenKind.ID])

    def test_lexer_7(self):
        l = Lexer('!Q)P!').tokenize()
        self.assertEqual(l.kind, [TokenKind.NOT, TokenKind.ID, TokenKind.RPAR,
            TokenKind.ID, TokenKind.NOT])

    def test_lexer_8(self):
        l = Lexer('A/\((B/\(C\/D))),A\/C').tokenize()
        self.assertEqual(l.kind, [TokenKind.ID, TokenKind.AND, TokenKind.LPAR,
            TokenKind.LPAR, TokenKind.ID, TokenKind.AND, TokenKind.LPAR,
            TokenKind.ID, TokenKind.OR, TokenKind.ID, TokenKind.RPAR,
            TokenKind.RPAR, TokenKind.RPAR, TokenKind.COMMA, TokenKind.ID,
            TokenKind.OR, TokenKind.ID])

    def test_lexer_9(self):
        l = Lexer('Q\./P').tokenize()
        self.assertEqual(l.kind, [TokenKind.ID, TokenKind.XOR, TokenKind.ID])

    def test_lexer_10(self):
        l = Lexer('(A/\B)\/C').tokenize()
        self.assertEqual(l.kind, [TokenKind.LPAR, TokenKind.ID, TokenKind.AND,
            TokenKind.ID, TokenKind.RPAR, TokenKind.OR, TokenKind.ID])

    def test_lexer_11(self):
        l = Lexer('B\/(C),A/\!B').tokenize()
        self.assertEqual(l.kind, [TokenKind.ID, TokenKind.OR, TokenKind.LPAR,
            TokenKind.ID, TokenKind.RPAR, TokenKind.COMMA, TokenKind.ID,
            TokenKind.AND, TokenKind.NOT, TokenKind.ID])

    def test_lexer_12(self):
        l = Lexer('P/\!Q,!P<=>!Q').tokenize()
        self.assertEqual(l.kind, [TokenKind.ID, TokenKind.AND, TokenKind.NOT,
            TokenKind.ID, TokenKind.COMMA, TokenKind.NOT, TokenKind.ID,
            TokenKind.IFF, TokenKind.NOT, TokenKind.ID])

    def test_lexer_13(self):
        l = Lexer('P /\ Q => P').tokenize()
        self.assertEqual(l.kind, [TokenKind.ID, TokenKind.AND, TokenKind.ID,
            TokenKind.IMPLIES, TokenKind.ID])

    ########### parser tests ###########

    def test_parser_1(self):
        tokelist = Lexer('Q').tokenize()
        parse_tree = Parser().parse(tokelist)
        self.assertEqual(parse_tree, ['propositions', 'proposition', 'atomic', 'ID', 'more-proposition', 'epsilon'])

    def test_parser_2(self):
        tokelist = Lexer('!Q').tokenize()
        parse_tree = Parser().parse(tokelist)
        self.assertEqual(parse_tree, ['propositions', 'proposition', 'compound', 'NOT', 'proposition', 'atomic', 'ID', 'more-proposition', 'epsilon'])

    def test_parser_3(self):
        tokelist = Lexer('P <=> Q').tokenize()
        parse_tree = Parser().parse(tokelist)
        self.assertEqual(parse_tree, ['propositions', 'proposition', 'compound', 'atomic', 'ID', 'connective', 'IFF', 'proposition', 'atomic', 'ID', 'more-proposition', 'epsilon'])

    def test_parser_4(self):
        tokelist = Lexer('( P /\ Q )').tokenize()
        parse_tree = Parser().parse(tokelist)
        self.assertEqual(parse_tree, ['propositions', 'proposition', 'compound',
           'LPAR', 'proposition', 'compound', 'atomic', 'ID', 'connective', 'AND', 'proposition', 'atomic', 'ID', 'RPAR', 'more-proposition', 'epsilon' ])

    def test_parser_5(self):
        tokelist = Lexer('( P \/ Q ) , ( X => Y )').tokenize()
        parse_tree = Parser().parse(tokelist)
        self.assertEqual(parse_tree, ['propositions', 'proposition', 'compound', 'LPAR',
            'proposition', 'compound', 'atomic', 'ID', 'connective', 'OR', 'proposition',
            'atomic', 'ID', 'RPAR', 'more-proposition', 'comma', 'propositions',
            'proposition', 'compound', 'LPAR', 'proposition', 'compound', 'atomic', 'ID',
            'connective', 'IMPLIES', 'proposition', 'atomic', 'ID', 'RPAR',
            'more-proposition', 'epsilon'])

    def test_parser_6(self):
        tokelist = Lexer(')Q').tokenize()
        parseTree = Parser().parse(tokelist)
        self.assertEqual(parseTree, 'Syntax Error at line 1 column 1.')

    def test_parser_7(self):
        tokelist = Lexer('!Q)P!').tokenize()
        parseTree = Parser().parse(tokelist)
        self.assertEqual(parseTree, 'Syntax Error at line 1 column 3.')

    def test_parser_8(self):
        tokelist = Lexer('A/\((B/\(C\/D))),A\/C').tokenize()
        parse_tree = Parser().parse(tokelist)
        self.assertEqual(parse_tree, ['propositions', 'proposition', 'compound',
            'atomic', 'ID', 'connective', 'AND', 'proposition', 'compound',
            'LPAR', 'proposition', 'compound', 'LPAR', 'proposition', 'compound',
            'atomic', 'ID', 'connective', 'AND', 'proposition', 'compound',
            'LPAR', 'proposition', 'compound', 'atomic', 'ID',
            'connective', 'OR', 'proposition', 'atomic', 'ID', 'RPAR', 'RPAR',
            'RPAR', 'more-proposition', 'comma', 'propositions', 'proposition',
            'compound', 'atomic', 'ID', 'connective', 'OR', 'proposition',
            'atomic', 'ID', 'more-proposition', 'epsilon'])

    def test_parser_9(self):
        tokelist = Lexer('Q\./P').tokenize()
        parse_tree = Parser().parse(tokelist)
        self.assertEqual(parse_tree, ['propositions', 'proposition', 'compound',
            'atomic', 'ID', 'connective', 'XOR', 'proposition', 'atomic', 'ID', 'more-proposition', 'epsilon'])

    def test_parser_10(self):
        tokelist = Lexer('(A/\B)\/C').tokenize()
        parseTree = Parser().parse(tokelist)
        self.assertEqual(parseTree, 'Syntax Error at line 1 column 6.')

    def test_parser_11(self):
        tokelist = Lexer('B\/(C),A/\!B').tokenize()
        parse_tree = Parser().parse(tokelist)
        self.assertEqual(parse_tree, ['propositions', 'proposition', 'compound',
            'atomic', 'ID', 'connective', 'OR', 'proposition', 'compound',
            'LPAR', 'proposition', 'atomic', 'ID', 'RPAR', 'more-proposition', 'comma',
            'propositions', 'proposition', 'compound', 'atomic', 'ID',
            'connective', 'AND', 'proposition', 'compound', 'NOT', 'proposition', 'atomic',
            'ID', 'more-proposition', 'epsilon'])

    def test_parser_12(self):
        tokelist = Lexer('P/\!Q,!P<=>!Q').tokenize()
        parse_tree = Parser().parse(tokelist)
        self.assertEqual(parse_tree, ['propositions', 'proposition', 'compound', 'atomic',
            'ID', 'connective', 'AND', 'proposition', 'compound', 'NOT', 'proposition', 'atomic',
            'ID', 'more-proposition', 'comma', 'propositions', 'proposition', 'compound', 'NOT',
            'proposition', 'compound', 'atomic', 'ID', 'connective', 'IFF', 'proposition', 'compound',
            'NOT', 'proposition', 'atomic', 'ID', 'more-proposition', 'epsilon'])

    def test_parser_13(self):
        tokelist = Lexer('P /\ Q => P').tokenize()
        parse_tree = Parser().parse(tokelist)
        self.assertEqual(parse_tree, ['propositions', 'proposition', 'compound', 'atomic',
            'ID', 'connective', 'AND', 'proposition', 'compound', 'atomic', 'ID', 'connective',
            'IMPLIES', 'proposition', 'atomic', 'ID', 'more-proposition', 'epsilon'])

    ############# Code Generation Tests ############



#    def test_codeGen_1(self):
#        tokelist = Lexer('Q').tokenize()
#        parse_tree = Parser().parse(tokelist)
#        #generated = CodeGen(tokelist, parse_tree).generate()
#
#    def test_codeGen_2(self):
#        tokelist = Lexer('!Q').tokenize()
#        parse_tree = Parser().parse(tokelist)
#        #generated = CodeGen(tokelist, parse_tree).generate()
#
#    def test_codeGen_3(self):
#        tokelist = Lexer('P <=> Q').tokenize()
#        parse_tree = Parser().parse(tokelist)
#        #generated = CodeGen(tokelist, parse_tree).generate()
#
#    def test_codeGen_4(self):
#        tokelist = Lexer('( P /\ Q )').tokenize()
#        parse_tree = Parser().parse(tokelist)
#        #generated = CodeGen(tokelist, parse_tree).generate()
#
#    def test_codeGen_5(self):
#        tokelist = Lexer('( P \/ Q ) , ( X => Y )').tokenize()
#        parse_tree = Parser().parse(tokelist)
#        #generated = CodeGen(tokelist, parse_tree).generate()
#
#    def test_codeGen_6(self):
#        tokelist = Lexer(')Q').tokenize()
#        parse_tree = Parser().parse(tokelist)
#        #generated = CodeGen(tokelist, parse_tree).generate()
#
#    def test_codeGen_7(self):
#        tokelist = Lexer('!Q)P!').tokenize()
#        parse_tree = Parser().parse(tokelist)
#        #generated = CodeGen(tokelist, parse_tree).generate()
#
#    def test_codeGen_8(self):
#        tokelist = Lexer('A/\((B/\(C\/D))),A\/C').tokenize()
#        parse_tree = Parser().parse(tokelist)
#        #generated = CodeGen(tokelist, parse_tree).generate()
#
#    def test_codeGen_9(self):
#        tokelist = Lexer('Q\./P').tokenize()
#        parse_tree = Parser().parse(tokelist)
#        #generated = CodeGen(tokelist, parse_tree).generate()
#
#    def test_codeGen_10(self):
#        tokelist = Lexer('(A/\B)\/C').tokenize()
#        parse_tree = Parser().parse(tokelist)
#        #generated = CodeGen(tokelist, parse_tree).generate()
#
#    def test_codeGen_11(self):
#        tokelist = Lexer('B\/(C),A/\!B').tokenize()
#        parse_tree = Parser().parse(tokelist)
#        generated = CodeGen(tokelist, parse_tree).generate()

    def test_codeGen_11(self):
        tokelist = Lexer('B\/(C)').tokenize()
        parse_tree = Parser().parse(tokelist)
        print tokelist
        print parse_tree
        generated = CodeGen(tokelist, parse_tree).generate()
#
#    def test_codeGen_12(self):
#        tokelist = Lexer('P/\!Q,!P<=>!Q').tokenize()
#        parse_tree = Parser().parse(tokelist)
#        print tokelist
#        print parse_tree
#        generated = CodeGen(tokelist, parse_tree).generate()


#    def test_codeGen_13(self):
#        tokelist = Lexer('P /\ Q => P').tokenize()
#        parse_tree = Parser().parse(tokelist)
#        print tokelist
#        print parse_tree
#        generated = CodeGen(tokelist, parse_tree).generate()

#print sys.argv

#if run as just main.py do unit tests
if __name__ == '__main__' and len(sys.argv) == 1:
    unittest.main()
#else take the input file and run it through lexer and parser
else:
    with open(sys.argv[1], 'r') as file:
        for index, line in enumerate(file):
            print line

            #Lexer
            l = Lexer(line)
            l.line = index + 1
            tokelist = l.tokenize()
            print tokelist.kind
            l.line += 1

            #Parser
            parse_tree = Parser().parse(tokelist)
            print parse_tree

            #Code Generator
            g = CodeGen(tokelist, parse_tree)
            satisiable = g.generate()
            print "\n----------\n"

