# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 15:36:06 2022

@author: Tuyen
"""

"""
This is a recursive descent parser for the happylang
language. 
To write a parser:
    1.) Construct the basic interface (lexer, next, has, must_be).
    2.) Convert each BNF rule into a mutually recursive function.
    3.) Add data structures to build the parse tree.
"""
from happylang_lexer import HappyLexer, Token, TokenDetail
import sys

class HappyParser:
    """
    Parser state will follow the lexer state.
    We consume the stream token by token.
    Match our tokens, if no match is possible, 
    print an error and stop parsing.
    """
    def __init__(self, lexer= HappyLexer()):
        self.__lexer = lexer
        
    def __next(self):
        """
        Advance/consume the next token
        """
        
        self.__cur_token_detail = self.__lexer.next()

    

    def __has(self, t):
        """
        Return true if t matches the current token.

        Parameters
        ----------
        t : Token 

        Returns
        -------
        bool
        
        """
        return self.__cur_token_detail.token == t
        
    
    def __must_be(self, t):
        """
        Return true if t matches the current token.
        Otherwise, we print an error message and
        exit.

        Parameters
        ----------
        t : Token 

        Returns
        -------
        bool

        """
        if (self.__has(t)):
            return True
        
        line = self.__cur_token_detail.line
        col = self.__cur_token_detail.col
        token = self.__cur_token_detail.token
        print(f"Parser error at line {line}, column {col}.\nReceived token {token.name} expected {t.name}")
        sys.exit(-1)
        
    def parse(self):
        self.__next()
        self.__program()
        
    def __program(self):
        """
        Pre: The next token has been consumed 

        """
        
        self.__main_fun()
        
        while not self.__has(Token.EOF):
            self.__fun()
            
    def __main_fun(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        """
        self.__must_be(Token.MAIN)
        self.__next()
        self.__must_be(Token.LPAREN)
        self.__next()
        self.__must_be(Token.RPAREN)
        self.__next()
        self.__block()
        
    def __fun(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        """
        self.__must_be(Token.IDENTIFIER)
        self.__next()
        self.__must_be(Token.LPAREN)
        self.__next()
        self.__fun2()
        
    def __fun2(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        """
        if self.__has(Token.RPAREN):
            self.__next()
            self.__block()
        else:
            self.__param_list()
            self.__must_be(Token.RPAREN)
            self.__next()
            self.__block()
        
     
    
    def __param_list(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        """
        self.__param_decl()
        
        while (self.__has(Token.COMMA)):
            self.__next()
            self.__param_decl()
            
    def __param_decl(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        """
        if self.__has(Token.NUMBER_TP):
            self.__next()
            self.__param_decl2()
        elif self.__has(Token.STRING_TP):
            self.__next()
            self.__param_decl2()
        else:
            self.__must_be(Token.NUMBER_TP)
        
        
    def __param_decl2(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        """
        if self.__has(Token.IDENTIFIER):
            self.__next()
        elif self.__has(Token.LBRACKET):
            self.__next()
            self.__must_be(Token.RBRACKET)
            self.__next()
            self.__must_be(Token.IDENTIFIER)
            self.__next()
        elif self.__has(Token.STACK):
            self.__next()
            self.__must_be(Token.IDENTIFIER)
            self.__next()
        else:
            self.__must_be(Token.IDENTIFIER)
            
    
    def __block(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        """
        self.__must_be(Token.LCURLY)
        self.__next()
        self.__var_stmt_list()
        self.__must_be(Token.RCURLY)
        self.__next()
        
    def __var_stmt_list(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        """
        while not self.__has(Token.RCURLY):
            if self.__has(Token.NUMBER_TP) or self.__has(Token.STRING_TP):
                self.__var_decl()
            else:
                self.__stmt()
                
                
    def __var_decl(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        """
        if self.__has(Token.NUMBER_TP):
            self.__next()
            self.__var_decl2()
            
        elif self.__has(Token.STRING_TP):
            self.__next()
            self.__var_decl2()
            
    def __var_decl2(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        """
        if self.__has(Token.IDENTIFIER):
            self.__next()
        elif self.__has(Token.LBRACKET):
            self.__next()
            self.__expr()
            self.__must_be(Token.RBRACKET)
            self.__next()
            self.__must_be(Token.IDENTIFIER)
            self.__next()
        elif self.__has(Token.STACK):
            self.__next()
            self.__must_be(Token.IDENTIFIER)
            self.__next()
        else:
            self.__must_be(Token.IDENTIFIER)
        
        
        
    def __stmt(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        """
        if self.__has(Token.IDENTIFIER):
            self.__id_stmt()
        elif self.__has(Token.IF):
            self.__branch()
        elif self.__has(Token.FOR):
            self.__for_loop()
        elif self.__has(Token.PRINT):
            self.__print()
        elif self.__has(Token.PRINTLN):
            self.__println()
        elif self.__has(Token.INPUT):
            self.__input()
        else:
            self.__expr()
        
        
    def __id_stmt(self):
        """
        Pre: The next token has been consumed and must be id
        Post: Consume the next token before leaving this function
        """
        self.__must_be(Token.IDENTIFIER)
        self.__ref()
        
        if self.__has(Token.ASSIGN):
            self.__next()
            self.__expr()
        elif self.__has(Token.SWAP):
            self.__next()
            self.__ref()
        elif self.__has(Token.DOT):
            self.__next()
            self.__stack_op()
        else:
            if self.__has(Token.LPAREN):
                self.__next()
                self.__call2()
            else:
                self.__factor2()
                self.__term2()
                self.__expr2()
            
            
    def __ref(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        """
        self.__must_be(Token.IDENTIFIER)
        self.__next()
        
        if self.__has(Token.LBRACKET):
            self.__next()
            self.__expr()
            self.__must_be(Token.RBRACKET)
            self.__next()
    
        
    def __stack_op(self):
        """
        Pre: The next token has been consumed and must be push or pop
        Post: Consume the next token before leaving this function
        """
        if self.__has(Token.PUSH):
            self.__next()
            self.__must_be(Token.LPAREN)
            self.__next()
            self.__expr()
            self.__must_be(Token.RPAREN)
        elif self.__has(Token.POP):
            self.__next()
            self.__must_be(Token.LPAREN)
            self.__next()
            self.__must_be(Token.RPAREN)
        
        else:
            self.__must_be(Token.PUSH)
            
        self.__next()

        
            
    def __branch(self):
        """
        Pre: The next token has been consumed and must be if
        Post: Consume the next token before leaving this function
        """
        self.__must_be(Token.IF)
        self.__next()
        self.__condition_list()
        self.__block()
        
        if self.__has(Token.ELSE):
            self.__next()
            self.__block()

        
        
    def __condition_list(self):
        """
        Pre: The next token has been consumed 
        Post: Consume the next token before leaving this function
        """
        self.__condition()
        self.__condition_list2()
        
    def __condition_list2(self):
        """
        Pre: The next token has been consumed 
        Post: Consume the next token before leaving this function
        """
        if self.__has(Token.AND):
            self.__next()
            self.__condition()
            self.__condition_list2()
        elif self.__has(Token.OR):
            self.__next()
            self.__condition()
            self.__condition_list2()
            
        
    def __condition(self):
        """
        Pre: The next token has been consumed 
        Post: Consume the next token before leaving this function
        """
        if self.__has(Token.LPAREN):
            self.__next()
            self.__condition_list()
            self.__must_be(Token.RPAREN)
            self.__next()
        else:
            self.__expr()
            self.__condition2()
            
    def __condition2(self):
        if self.__has(Token.EQ) or self.__has(Token.NE) or self.__has(Token.LT) or self.__has(Token.LE) or self.__has(Token.GT) or self.__has(Token.GE):
            self.__next()
            self.__expr()
            
        else:
            self.__must_be(Token.EQ)
        
    def __for_loop(self):
        
        """
        Pre: The next token has been consumed and must be for
        Post: Consume the next token before leaving this function
        """
        self.__must_be(Token.FOR)
        self.__next()
        self.__must_be(Token.LPAREN)
        self.__next()
        if not self.__has(Token.SEMICOLON):
            self.__assign_list()
        self.__must_be(Token.SEMICOLON)
        self.__next()
        self.__condition_list()
        self.__must_be(Token.SEMICOLON) 
        self.__next()
        if not self.__has(Token.RPAREN):
            self.__assign_list()
        self.__must_be(Token.RPAREN)
        self.__next()
        self.__block()     
        
    def __assign_list(self):
       self.__assign()
        
       while self.__has(Token.COMMA):
           self.__next()
           self.__assign()
           
    def __assign(self):
       self.__ref()
       self.__must_be(Token.ASSIGN)
       self.__next()
       self.__expr()
        
        
    def __expr(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        """
        self.__term()
        self.__expr2()
        
    def __expr2(self):
        if self.__has(Token.PLUS):
            self.__next()
            self.__term()
            self.__expr2()
            
        elif self.__has(Token.MINUS):
            self.__next()
            self.__term()
            self.__expr2()
        
    def __term(self):
        self.__factor()
        self.__term2()
        
    def __term2(self):
        if self.__has(Token.TIMES):
            self.__next()
            self.__factor()
            self.__term2()
        elif self.__has(Token.DIVISION):
            self.__next()
            self.__factor()
            self.__term2()
    
    def __factor(self):
        if self.__has(Token.MINUS):        
            self.__next()
            
        self.__exponent()
        self.__factor2()
        
    def __factor2(self):
        if self.__has(Token.POWER):
            self.__next()
            self.__factor()
            
    def __exponent(self):
        if self.__has(Token.LPAREN):
            self.__next()
            self.__expr()
            self.__must_be(Token.RPAREN)
            self.__next()
        elif self.__has(Token.IDENTIFIER):
            self.__ref_or_call()
        elif self.__has(Token.NUMBER):
            self.__next()
        elif self.__has(Token.STRING):
            self.__next()
        elif self.__has(Token.LEN):
            self.__next()
            self.__must_be(Token.LPAREN)
            self.__next()
            self.__must_be(Token.IDENTIFIER)
            self.__next()
            self.__must_be(Token.RPAREN)
            self.__next()
            
    def __ref_or_call(self):
        self.__must_be(Token.IDENTIFIER)
        self.__next()
        
        print(self.__cur_token_detail)

        if self.__has(Token.LBRACKET):
            self.__next()
            self.__expr()
            self.__must_be(Token.RBRACKET)
            self.__next()
        elif self.__has(Token.LPAREN):
            self.__next()
            self.__call2()
            
    def __call2(self):
        if self.__has(Token.RPAREN):
            self.__next()
        else:
            self.__arg_list()
            self.__must_be(Token.RPAREN)
            self.__next()
        
    def __input(self):
        """
        Pre: The next token has been consumed and must be for
        Post: Consume the next token before leaving this function
        """
        self.__must_be(Token.INPUT)
        self.__next()
        self.__input2()
        
    def __input2(self):
        if self.__has(Token.STRING):
            self.__next()
            self.__must_be(Token.SEMICOLON)
            self.__next()
       
        self.__ref_list()
        
    def __ref_list(self):
        self.__ref()
        
        while self.__has(Token.COMMA):
            self.__next()
            self.__ref()
        
        
    def __print(self):
        self.__must_be(Token.PRINT)
        self.__next()
        self.__arg_list()
        
    
    def __println(self):
        self.__must_be(Token.PRINTLN)
        self.__next()
        self.__arg_list()
        
    def __arg_list(self):
        self.__expr()
        
        while self.__has(Token.COMMA):
            self.__next()
            self.__expr()
            
            
            
# unit test 
if __name__ == "__main__":
    p = HappyParser()
    p.parse()
        
    
        
        
        
            
    
            
        
    
    
    
        