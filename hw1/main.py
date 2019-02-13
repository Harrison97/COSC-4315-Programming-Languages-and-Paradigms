import unittest
import sys
from lexer import Lexer, TokenKind
from parser import Parser


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
        with self.assertRaises(SyntaxError) as err:
            Parser().parse(tokelist)
        self.assertEqual(str(err.exception), str(SyntaxError('Syntax Error at line 1 column 1.')))

    def test_parser_7(self):
        tokelist = Lexer('!Q)P!').tokenize()
        with self.assertRaises(SyntaxError) as err:
            Parser().parse(tokelist)
        self.assertEqual(str(err.exception), str(SyntaxError('Syntax Error at line 1 column 3.')))

#print sys.argv

#if run as just main.py do unit tests
if __name__ == '__main__' and len(sys.argv) == 1:
    unittest.main()
#else take the input file and run it through lexer and parser
else:
    with open(sys.argv[1], 'r') as file:
        for index, line in enumerate(file):
            l = Lexer(line)
            l.line = index + 1
            tokelist = l.tokenize()
            #print tokelist.kind
            l.line += 1
            parse_tree = Parser().parse(tokelist)
            #print parse_tree

