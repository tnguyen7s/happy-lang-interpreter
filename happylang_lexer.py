# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 21:21:05 2022

@author: Tuyen
"""

"""
This module contains a lexer for the happy language.
To Write a Lexer
1.) Implement Scanning
    - Scan character by character (Theory requirement)
    - Keep track of line and column number (Practical requirement)
    - implement a function to skip spaces (Practical Requirement)
    
2.) Implement Tokens
    2.1) Identify the regular portions of our grammar.
         - All terminals are automatically regular. (A -> a)
         - Look out for regular rules:
             A->aA     -or-     A->Aa
    2.2) Separate the tokens out of our parser grammar, and build
         the lexer grammar.
    2.3) Create a representation for all the tokens.
         - be sure to add two "utility" tokens as a practacial 
           requirement: INVALID, EOF
           
3.) Implement a way to get token details.
    - token: numerical category of the lexed item
    - lexeme: Actual characters that were matched
    - value: numeric value of the lexeme
    - line: Line number where the token begins
    - col: Column where the token begins
    NOTE: Token details are immutable.
    
4.) Implement the "next" function which consumes and returns
    the next matched token detail structure.
    Group Tokens into the following categories:
    1.) Single character tokens which are not the prefix of any other
        token.
    2.) Multiple-Character tokens where each token is of fixed length
        and there may be common prefixes. (The token shares no 
        prefix in common with a group 3 token.)
    3.) Everything else (variable width)
        - usually requires a customized approach
        - Consume until an inconsistency is reached.
        - Match any fixed tokens
        - Implementing a finite state machine
"""

from enum import Enum, auto
import sys
from collections import namedtuple

class Token(Enum):
    MAIN = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    PUSH = auto()
    POP = auto()
    LEN = auto()
    PRINT = auto()
    PRINTLN = auto()
    INPUT = auto()
    NUMBER_TP = auto() 
    STRING_TP = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LCURLY = auto()
    RCURLY = auto()
    COMMA = auto()
    SEMICOLON = auto()
    DOT = auto()
    PIPE = auto()
    ASSIGN = auto()
    SWAP = auto()
    AND = auto()
    OR = auto()
    STACK = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVISION = auto()
    MOD = auto()
    POWER = auto()


    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    
    INVALID = auto()
    EOF = auto()
    
    RETURN = auto()
    
    
TokenDetail = namedtuple('TokenDetail', ['token', 'lexeme', 'value', 'line', 'col'])
class HappyLexer:
    '''
    The lexer class for the happy language. 
    Converts a text stream into a token stream
    '''
    def __init__(self, lex_file = sys.stdin):
        self.__lex_file = lex_file
        self.__line = 1
        self.__col = 0
        self.__cur_char = None
        
        # scan the first character
        self.__consume()
        
        # store the current token
        self.__token_detail = TokenDetail(Token.INVALID, '', None, 0, 0)
        
    def __consume(self):
        """
        Consumes a character from the stream, and 
        makes it the lexer's current character

        Returns
        -------
        None.

        """
        self.__cur_char = self.__lex_file.read(1)
        self.__col += 1
        
        if (self.__cur_char=='\n'):
            self.__line += 1
            self.__col = 0
            
    def __skip_spaces_and_comments(self):
        """
        Consumes characters until we encounter non-whitespace.
        Also, skips comments
        Also, stops on end of file
        End of this, consume one character ahead
        Returns
        -------
        None.

        """
        """
        while self.__cur_char == '#' or self.__cur_char == ' ' or self.__cur_char=='\n':
            if self.__cur_char == '#':
                while self.__cur_char != '\n':
                    self.__consume()
            else:
                while  self.__cur_char == ' ':
                    self.__consume()
                    
            if (self.__cur_char == '\n'):
                self.__consume()
        """
        while self.__cur_char.isspace() or self.__cur_char == '#':
            if self.__cur_char == '#':
                # consume the rest of the line
                while self.__cur_char and self.__cur_char != '\n':
                    self.__consume()

            # consume all the whitespace
            while self.__cur_char.isspace():
                self.__consume()

                
    def __create_tok(self, token, lexeme=None, value=None, line=None, col=None):
        """
        Create a TokenDetail
        If no lexeme, line, or col provided, use the lexer's current char, line, and col
        Returns
        -------
        TokenDetail

        """
        if not lexeme:
            lexeme = self.__cur_char
        
        if not line:
            line = self.__line
            
        if not col:
            col = self.__col
            
        return TokenDetail(token, lexeme, value, line, col)
    
    def __lex_single(self):
        """
        Recognize group 1 tokens. (Single character tokens which are not prefix of any other tokens.)

        Returns
        -------
        bool
            True if match otherwise False.

        """
        singles = {'(': Token.LPAREN, 
                   ')': Token.RPAREN, 
                   '[': Token.LBRACKET, 
                   ']': Token.RBRACKET, 
                   '{': Token.LCURLY, 
                   '}': Token.RCURLY, 
                   ',': Token.COMMA, 
                   ';': Token.SEMICOLON, 
                   '.': Token.DOT, 
                   '=': Token.EQ, 
                   '+': Token.PLUS, 
                   '-': Token.MINUS,
                   '/': Token.DIVISION, 
                   '%': Token.MOD}
        
        if self.__cur_char in singles:
            self.__token_detail = self.__create_tok(singles[self.__cur_char])
            self.__consume()
            return True
        
        return False
    
    def __lex_multi_fixed(self):
        """
        Attempt to match multi-character tokens which may overlap in prefix.

        Returns
        -------
        bool.
            True if match otherwise return False
        """        
        line = self.__line
        col = self.__col
        cur_lex = ""
        
        list_ = {':=': Token.ASSIGN, 
                 ':=:': Token.SWAP, 
                 '&&': Token.AND, 
                  '|': Token.PIPE, 
                 '||': Token.OR, 
                 '|_|': Token.STACK,
                 '<>': Token.NE, 
                 '<': Token.LT, 
                 '<=': Token.LE, 
                 '>': Token.GT, 
                 '>=': Token.GE, 
                 '*': Token.TIMES, 
                 '**': Token.POWER}
        
        i = 0
        while len(list_)!=0:
            list_old = list_.copy()
            for t in list_old.keys():
                if i>=len(t) or self.__cur_char != t[i]:
                    del list_[t]
                                
            if len(list_)!=0:
                cur_lex += self.__cur_char
                i += 1
                self.__consume()
        
        # token found
        if cur_lex in list_old:
            v = list_old[cur_lex]
            
            self.__token_detail = self.__create_tok(v, lexeme=cur_lex, line=line, col=col)
            return True
                
        # incomplete token
        if i!=0:
            self.__token_detail = self.__create_tok(Token.INVALID, line=line, col=col)
            return True
        
        return False
    
    def __lex_other(self):
        if self.__cur_char.isdigit():
            return self.__lex_number()
            
        elif self.__cur_char == '"':
            return self.__lex_string()
        
        elif self.__cur_char.isalpha() or self.__cur_char=='_':
            return self.__lex_identifier_and_kw()
        
        return False
    
    
    def __lex_number(self):   
        """
        Lex a number, enter the function when self.__cur_char.isdigit()

        Returns
        -------
        bool
            True.

        """
        line = self.__line
        col = self.__col
        cur_lex = ""
        
        while (self.__cur_char.isdigit()):
            cur_lex += self.__cur_char
            self.__consume()
            
        if (self.__cur_char == '.'):
            cur_lex += self.__cur_char
            self.__consume()
            while (self.__cur_char.isdigit()):
                cur_lex += self.__cur_char
                self.__consume()
            
        self.__token_detail = self.__create_tok(Token.NUMBER, lexeme=cur_lex, value = float(cur_lex), line=line, col=col)
        
        return True
    
    def __lex_string(self):
        """
        Lex a string, given self.__cur_char = '"'

        Returns
        -------
        bool.
            True 

        """
        line = self.__line
        col = self.__col
        cur_lex = '"'
        
        self.__consume()
        while self.__cur_char and self.__cur_char!='"':
            cur_lex += self.__cur_char
            self.__consume()
            
        if self.__cur_char == '"':
            cur_lex += self.__cur_char
            self.__consume()
            
            self.__token_detail = TokenDetail(Token.STRING, lexeme = cur_lex[1:-1], value=cur_lex[1:-1], line=line, col=col)
            return True
        
        
        self.__token_detail = TokenDetail(Token.INVALID, lexeme = cur_lex, value=None, line=line, col=col)
        return True
    
    def __lex_identifier_and_kw(self):
        kw = {'main' : Token.MAIN,
              'if': Token.IF,
              'else': Token.ELSE,
              'for': Token.FOR,
              'push': Token.PUSH,
              'pop': Token.POP,
              'len': Token.LEN, 
              'print': Token.PRINT,
              'println': Token.PRINTLN,
              'input': Token.INPUT,
              'NUMBER': Token.NUMBER_TP,
              'STRING': Token.STRING_TP, 
              'return': Token.RETURN}
        
        line = self.__line
        col = self.__col
        cur_lex = ""
        
        while self.__cur_char.isalpha() or self.__cur_char == '_' or self.__cur_char.isdigit():
            cur_lex += self.__cur_char
            self.__consume()
            
        
        if cur_lex in kw:
            self.__token_detail = self.__create_tok(kw[cur_lex], lexeme=cur_lex, line=line, col=col)
            return True
        
        self.__token_detail = self.__create_tok(Token.IDENTIFIER, lexeme=cur_lex, line=line, col=col)
        return True
                
    def next(self):
        """
        Advance the lexer to the next token and return that token

        Returns
        -------
        TokenDetail.

        """
        self.__skip_spaces_and_comments()
        
        if not self.__cur_char:
            self.__token_detail = self.__create_tok(Token.EOF)
            return self.__token_detail 
        elif self.__lex_single():
            return self.__token_detail
        elif self.__lex_multi_fixed():
            return self.__token_detail
        elif self.__lex_other():
            return self.__token_detail
        
        # else invalid
        self.__token_detail = self.__create_tok(Token.INVALID)
        self.__consume()
        
        return self.__token_detail
    
    def get_tok(self):
         """
         Return current token

         Returns
         -------
         TokenDetail

         """
         return self.__token_detail
    
if __name__ == '__main__':
    lex = HappyLexer()
    while lex.get_tok().token != Token.EOF:
        #lex.__skip_space_and_comments()
        #lex.__consume()
        #print("Line %d Col %d: %s" % (lex.get_line(), lex.get_col(), lex.get_char()))
        print(lex.next())
        
        
        
        
        
                    
            

            
    
            
