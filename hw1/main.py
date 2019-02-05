import unittest
from lexer import Lexer, TokenKind
from parser import Parser




class Test(unittest.TestCase):
    def test1(self):
        l = Lexer('Q').tokenize()
        self.assertEqual(l.kind, [TokenKind.ID])

    def test5(self):
        l = Lexer('!Q').tokenize()
        self.assertEqual(l.kind, [TokenKind.NOT, TokenKind.ID])
    
    def test6(self):
        l = Lexer('(=>)').tokenize()
        self.assertEqual(l.kind, [TokenKind.LPAR, TokenKind.IMPLIES, TokenKind.RPAR])

    def test7(self):
        l = Lexer('(<=>)').tokenize()
        self.assertEqual(l.kind, [TokenKind.LPAR, TokenKind.IFF, TokenKind.RPAR])




    def test2(self):
        tokelist = Lexer('Q').tokenize()
        parse_tree = Parser().parse(tokelist)
    #     some assertion goes here
    
    # def test3(self):
    #     tokelist = Lexer('Q').tokenize()
    #     #parse_tree = Parser().parse(tokelist)
    #     # some assertion goes here

    # def test4(self):
    #     tokelist = Lexer('Q').tokenize()
    #     #parse_tree = Parser().parse(tokelist)
    #     # some assertion goes here


if __name__ == '__main__':
    unittest.main()


