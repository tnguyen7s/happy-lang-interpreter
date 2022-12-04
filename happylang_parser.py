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
from enum import Enum, auto

class ParseType(Enum):
    PROGRAM = auto()
    BLOCK = auto() # multiple stmts
    ATOMIC = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    POW = auto()
    NEG = auto()
    LEN = auto()
    INDEXING = auto()
    CALL = auto()
    VAR = auto()
    ASSIGN = auto()
    SWAP = auto()
    PUSH = auto()
    POP = auto()
    IF = auto()
    IFELSE = auto()
    AND = auto()
    OR = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    LOOP = auto()
    PRINT = auto()
    PRINTLN = auto()
    INPUT = auto()
    FUN = auto()
    PARAM = auto()
    MAIN = auto()
    RETURN = auto()

    
ariness = {
            ParseType.ADD: 2,
            ParseType.SUB: 2,
            ParseType.MUL: 2,
            ParseType.DIV: 2,
            ParseType.MOD: 2,
            ParseType.AND: 2,
            ParseType.OR: 2
          }

class RefType(Enum):
    FUN = auto()
    PRIMITIVE = auto()
    ARRAY = auto()
    STACK = auto()
    

class ParseTree:
    """
    Tree of a parse type that will be evalutated by the happy lang interpreter\n
    
    Parameters
    ----------
    parse_type: The ParseType of the root of the tree
    token_detail: TokenDetail
    children: ParseTree[]
    """
    def __init__(self, parse_type=ParseType.PROGRAM, token_detail=None, ref_type = None):
        self.parse_type = parse_type
        self.token_detail = token_detail
        self.ref_type = ref_type
        self.children = []

        
    def print_tree(self, level=0):
        """
        Print the tree horizonally 
        right to left of an abnomal tree will be drawned from top to bottom,
        the root of the tree is located at the middle row
        """
        m = int(len(self.children)/2)-1
        
        # right haft
        for tree in self.children[-1:m:-1]:
            tree.print_tree(level+2)
            
            
        # the root
        indentation = "  "*level
        if self.parse_type in [ParseType.ATOMIC, ParseType.FUN]:
            print(indentation, self.token_detail.lexeme, sep='')
        elif self.parse_type in [ParseType.VAR, ParseType.PARAM]:
            print(indentation, self.ref_type.name, sep='')
        else:
            print(indentation, self.parse_type.name, sep='')
        
        # left half
        for tree in self.children[m::-1]:
            tree.print_tree(level+2)
    
    def children_extend_left(self, parse_trees):
        """
        Extend at the front of children
        
        Parameters
        ----------
        parse_tree : ParseTree[]

        Returns
        -------
        None.

        """
        self.children = parse_trees + self.children
 
    def children_extend_right(self, parse_trees):
        """
        Extend at the back of children
        
        Parameters
        ----------
        parse_trees : ParseTree[]

        Returns
        -------
        None.

        """
        self.children =  self.children + parse_trees
        
    def children_append_left(self, parse_tree):
        """
        Insert at the front of children

        Parameters
        ----------
        parse_tree : ParseTree

        Returns
        -------
        None.

        """
        self.children.insert(0, parse_tree)
        
    def children_append_right(self, parse_tree):
        """
        Insert at the back of children

        Parameters
        ----------
        parse_tree : ParseTree

        Returns
        -------
        None.

        """
        self.children.append(parse_tree)
        
    def insert_left_leaf(self, parse_tree):
        """
        insert into the left most of the tree

        Parameters
        ----------
        parse_tree : ParseTree

        Returns
        -------
        None.

        """
        if len(self.children) < ariness[self.parse_type]:
            self.children.insert(0, parse_tree)
        else:
            self.children[0].insert_left_leaf(parse_tree)
    
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
        return self.__program()
        
    def __program(self):
        """
        Pre: The next token has been consumed 

        """
        tree = ParseTree(ParseType.PROGRAM, self.__lexer.get_tok())
        
        # main function will be evaluated last
        tree.children_append_right(self.__main_fun())
        
        while not self.__has(Token.EOF):
            tree.children_append_right(self.__fun())
        
        return tree
            
    def __main_fun(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree(ParseType.FUN)
        """
        self.__must_be(Token.MAIN)
        tree = ParseTree(ParseType.MAIN, self.__lexer.get_tok())
        
        self.__next()
        self.__must_be(Token.LPAREN)
        self.__next()
        self.__must_be(Token.RPAREN)
        self.__next()
        
        
        tree.children_append_right(self.__block())
        return tree
        
    def __fun(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree(ParseType.FUN)
        """        
        self.__must_be(Token.IDENTIFIER)
        tree = ParseTree(ParseType.FUN, self.__lexer.get_tok())
        
        self.__next()
        self.__must_be(Token.LPAREN)
        
        self.__next()
        tree.children_extend_right(self.__fun2())
        
        return tree
    def __fun2(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        
        ParseTree []
        """
        trees = []
        
        if self.__has(Token.RPAREN):
            self.__next()
            trees.append(self.__block())
            
        else:
            trees.extend(self.__param_list())
            self.__must_be(Token.RPAREN)
            self.__next()
            trees.append(self.__block())

            
        return trees
        
     
    
    def __param_list(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree(ParseType.PARAM) []
        """
        trees = []
        trees.append(self.__param_decl())
        
        while (self.__has(Token.COMMA)):
            self.__next()
            trees.append(self.__param_decl())
            
        return trees
            
    def __param_decl(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree(ParseType.PARAM)
        """
        tree = None
        if self.__has(Token.NUMBER_TP):
            child = ParseTree(ParseType.ATOMIC, self.__lexer.get_tok())
            
            self.__next()
            tree = self.__param_decl2()
            tree.children_append_left(child)
        elif self.__has(Token.STRING_TP):
            child = ParseTree(ParseType.ATOMIC, self.__lexer.get_tok())
            
            self.__next()
            tree = self.__param_decl2()
            tree.children_append_left(child)
        else:
            self.__must_be(Token.NUMBER_TP)
            
        return tree 
    def __param_decl2(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree(ParseType.PARAM)
        """
        tree = ParseTree(ParseType.PARAM, self.__lexer.get_tok())
        
        if self.__has(Token.IDENTIFIER):
            tree.ref_type = RefType.PRIMITIVE
            child = ParseTree(ParseType.ATOMIC, self.__lexer.get_tok())
            tree.children_append_right(child)
            
            self.__next()
        elif self.__has(Token.LBRACKET):
            tree.ref_type = RefType.ARRAY
            
            self.__next()
            self.__must_be(Token.RBRACKET)
            
            self.__next()
            self.__must_be(Token.IDENTIFIER)
            child = ParseTree(ParseType.ATOMIC, self.__lexer.get_tok())
            tree.children_append_right(child)

            self.__next()
        elif self.__has(Token.STACK):
            tree.ref_type = RefType.STACK
            
            self.__next()
            self.__must_be(Token.IDENTIFIER)
            child = ParseTree(ParseType.ATOMIC, self.__lexer.get_tok())
            tree.children_append_right(child)
            
            self.__next()
        else:
            self.__must_be(Token.IDENTIFIER)
        
        return tree
    
    def __block(self):
        """
        v
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree(ParseType.BLOCK)
        """
        tree = ParseTree(ParseType.BLOCK, self.__lexer.get_tok())
        
        self.__must_be(Token.LCURLY)
        self.__next()
        
        tree.children_extend_right(self.__var_stmt_list())
        
        self.__must_be(Token.RCURLY)
        self.__next()
        
        return tree
        
    def __var_stmt_list(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree[]
        """
        trees = []
        
        while not self.__has(Token.RCURLY):
            if self.__has(Token.NUMBER_TP) or self.__has(Token.STRING_TP):
                trees.extend(self.__var_decl())
            else:
                trees.append(self.__stmt())
        
        return trees
                
    def __var_decl(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree [] (ParseType.VAR or ASSIGN) 
        """
        trees = []
        if self.__has(Token.NUMBER_TP) or self.__has(Token.STRING_TP):
            child = ParseTree(ParseType.ATOMIC, self.__lexer.get_tok())
            
            self.__next()
            tree1 = self.__var_decl2()
            tree1.children_append_left(child)
            trees.append(tree1)
            
            if self.__has(Token.ASSIGN):
                tree2 = ParseTree(ParseType.ASSIGN, self.__lexer.get_tok())
                
                self.__next()
                tree2.children_extend_right([tree1.children[1], self.__expr()])
                
                trees.append(tree2)
            
            
        return trees
            
    def __var_decl2(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree(ParseType.VAR) 
        """
        tree = ParseTree(ParseType.VAR, self.__lexer.get_tok())
        
        if self.__has(Token.IDENTIFIER):
            tree.ref_type = RefType.PRIMITIVE 
            
            child = ParseTree(ParseType.ATOMIC, self.__lexer.get_tok())
            tree.children_append_right(child)
            
            self.__next()
        elif self.__has(Token.LBRACKET):
            tree.ref_type = RefType.ARRAY
            
            self.__next()
            if self.__has(Token.RBRACKET):
                self.__must_be(Token.NUMBER)
                
            child2 = self.__expr()
            self.__must_be(Token.RBRACKET)
            
            self.__next()
            self.__must_be(Token.IDENTIFIER)
            child1 = ParseTree(ParseType.ATOMIC, self.__lexer.get_tok())
            tree.children_append_left(child1)
            tree.children_append_right(child2)

            self.__next()
        elif self.__has(Token.STACK):
            tree.ref_type = RefType.STACK 
            
            self.__next()
            self.__must_be(Token.IDENTIFIER)
            child = ParseTree(ParseType.ATOMIC, self.__lexer.get_tok())
            tree.children_append_right(child)

            self.__next()
        else:
            self.__must_be(Token.IDENTIFIER)
        
        return tree
        
    def __stmt(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree
        """
        if self.__has(Token.IDENTIFIER):
            return self.__id_stmt()
        if self.__has(Token.IF):
            return self.__branch()
        elif self.__has(Token.FOR):
            return self.__for_loop()
        elif self.__has(Token.PRINT):
            return self.__print()
        elif self.__has(Token.PRINTLN):
            return self.__println()
        elif self.__has(Token.INPUT):
            return self.__input()
        elif self.__has(Token.RETURN):
            return self.__return()
        else:
            return self.__expr()
    
    def __return(self):
        tree = ParseTree(ParseType.RETURN, self.__lexer.get_tok())
        
        self.__next()
        tree.children_append_right(self.__expr())
        
        return tree 
        
    def __id_stmt(self):
        """
        Pre: The next token has been consumed and must be id
        Post: Consume the next token before leaving this function
        """
        tree = None
        
        self.__must_be(Token.IDENTIFIER)
        child1 = self.__ref()
        
        if self.__has(Token.ASSIGN):
            tree = ParseTree(ParseType.ASSIGN, self.__lexer.get_tok())
            self.__next()
            
            child2 = self.__expr()
            tree.children_extend_right([child1, child2])
        elif self.__has(Token.SWAP):
            tree = ParseTree(ParseType.SWAP, self.__lexer.get_tok())
            self.__next()
            
            child2 = self.__ref()
            tree.children_extend_right([child1, child2])
        elif self.__has(Token.DOT):
            self.__next()
            
            tree = self.__stack_op()
            tree.children_append_left(child1)
        else:
            # incomplete implementation
            if self.__has(Token.LPAREN):
                self.__next()
                
                ref_leaf = child1
                tree = ParseTree(ParseType.CALL, self.__lexer.get_tok())
                tree.children_append_left(ref_leaf)
                tree.children_extend_right(self.__call2())  
                
            else:
                self.__factor2()
                self.__term2()
                self.__expr2()
            
            
        return tree
            
            
    def __ref(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree(ParseType.ATOMIC) or ParseTree(ParseType.INDEXING)
        """
        self.__must_be(Token.IDENTIFIER)
        
        ref = self.__lexer.get_tok()
        tree = ParseTree(ParseType.ATOMIC, ref)
        
        self.__next()
        
        if self.__has(Token.LBRACKET):
            self.__next()
            
            ref_leaf = tree
            loc_leaf = self.__expr()
            tree = ParseTree(ParseType.INDEXING, ref)
            tree.children_extend_right([ref_leaf, loc_leaf])
            
            self.__must_be(Token.RBRACKET)
            self.__next()
        
        return tree
        
    def __stack_op(self):
        """
        Pre: The next token has been consumed and must be push or pop
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree(ParseType.PUSH) or ParseTree(ParseType.POP)
        """
        tree = None
        
        if self.__has(Token.PUSH):
            tree = ParseTree(ParseType.PUSH, self.__lexer.get_tok())
            
            self.__next()
            self.__must_be(Token.LPAREN)
            
            self.__next()
            child = self.__expr()
            tree.children_append_right(child)
            
            self.__must_be(Token.RPAREN)
        elif self.__has(Token.POP):
            tree = ParseTree(ParseType.POP, self.__lexer.get_tok())
            
            self.__next()
            self.__must_be(Token.LPAREN)
            
            self.__next()
            self.__must_be(Token.RPAREN)
        else:
            self.__must_be(Token.POP)
            
        self.__next()
        return tree

        
            
    def __branch(self):
        """
        Pre: The next token has been consumed and must be if
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree(ParseType.IF)
        """
        self.__must_be(Token.IF)
        tree = ParseTree(ParseType.IF, self.__lexer.get_tok())
        
        self.__next()
        cond = self.__condition_list()
        b1 = self.__block()
        tree.children_append_left(cond)
        tree.children_append_right(b1)
        
        if self.__has(Token.ELSE):
            tree = ParseTree(ParseType.IFELSE, self.__lexer.get_tok())
            
            self.__next()
            b2 = self.__block()
            tree.children_append_left(cond)
            tree.children_extend_right([b1,b2])
            
        return tree

        
        
    def __condition_list(self):
        """
        Pre: The next token has been consumed 
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree(ParseType.AND)
        """
        child = self.__condition()
        
        tree = self.__condition_list2()
        
        if tree:
            tree.insert_left_leaf(child)
        else: 
            tree = child
            
        return tree
        
    def __condition_list2(self):
        """
        Pre: The next token has been consumed 
        Post: Consume the next token before leaving this function
        
        Returns
        -------------
        ParseTree(ParseType.AND)
        """
        tree = None
        if self.__has(Token.AND) or self.__has(Token.OR):
            tree = ParseTree(ParseType.AND, self.__lexer.get_tok()) if self.__has(Token.AND, ) else ParseTree(ParseType.OR, self.__lexer.get_tok())
            
            self.__next()
            child = self.__condition()
            tree.children_append_left(child)
            
            cond_list_root = self.__condition_list2()
            if cond_list_root:
                cond_list_root.insert_left_leaf(tree)
                tree = cond_list_root
            
        return tree
            
        
    def __condition(self):
        """
        Pre: The next token has been consumed 
        Post: Consume the next token before leaving this function
        
        Returns
        -------------
        ParseTree(ParseType.EQ)
        """
        tree = None
        if self.__has(Token.LPAREN):
            self.__next()
            tree = self.__condition_list()
            self.__must_be(Token.RPAREN)
            self.__next()
        else:
            child = self.__expr()
            tree = self.__condition2()
            
            tree.children_append_left(child)
            
        return tree
            
    def __condition2(self):
        """
        
        Returns
        -------------
        ParseTree(ParseType.EQ)
        """
        
        tree = None
        if self.__has(Token.EQ) or self.__has(Token.NE) or self.__has(Token.LT) or self.__has(Token.LE) or self.__has(Token.GT) or self.__has(Token.GE):
            if self.__has(Token.EQ):
                tree = ParseTree(ParseType.EQ, self.__lexer.get_tok())
            elif self.__has(Token.NE):
                tree = ParseTree(ParseType.NE, self.__lexer.get_tok())
            elif self.__has(Token.LT):
                tree = ParseTree(ParseType.LT, self.__lexer.get_tok())
            elif self.__has(Token.GT):
                tree = ParseTree(ParseType.GT, self.__lexer.get_tok())
            elif self.__has(Token.LE):
                tree = ParseTree(ParseType.LE, self.__lexer.get_tok())
            else:
                tree = ParseTree(ParseType.GE, self.__lexer.get_tok())
            
            self.__next()
            child = self.__expr()
            tree.children_append_right(child)
            
        else:
            self.__must_be(Token.EQ)
            
        return tree
        
    def __for_loop(self):
        
        """
        Pre: The next token has been consumed and must be for
        Post: Consume the next token before leaving this function
        
        Returns
        -------------
        ParseTree(ParseType.LOOP)
        """
        self.__must_be(Token.FOR)
        tree = ParseTree(ParseType.LOOP, self.__lexer.get_tok())
        
        self.__next()
        self.__must_be(Token.LPAREN)
        self.__next()
        if not self.__has(Token.SEMICOLON):
            tree.children_extend_left(self.__assign_list())
            
        self.__must_be(Token.SEMICOLON)
        self.__next()
        tree.children_append_right(self.__condition_list())
        self.__must_be(Token.SEMICOLON) 
        self.__next()
        if not self.__has(Token.RPAREN):
            tree.children_extend_right(self.__assign_list())
        self.__must_be(Token.RPAREN)
        self.__next()
        
        tree.children_append_right(self.__block())
        
        return tree
        
    def __assign_list(self):
       """
       Returns
       -------------
       ParseTree[]

       """
       trees = []
       
       trees.append(self.__assign())
        
       while self.__has(Token.COMMA):
           self.__next()
           trees.append(self.__assign())
           
       return trees
           
           
    def __assign(self):
        """
        Returns
        -------------
        ParseTree

        """
        child1 = self.__ref()
        
        self.__must_be(Token.ASSIGN)
        tree = ParseTree(ParseType.ASSIGN, self.__lexer.get_tok())
        
        self.__next()
        child2 = self.__expr()
        tree.children_extend_right([child1, child2])
        
        return tree
        
        
    def __expr(self):
        """
        Pre: The next token has been consumed
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree(ParseType.ADD) or ParseTree(ParseType.SUB)
        """
        child = self.__term()
        tree = self.__expr2()
        
        if tree:
            tree.insert_left_leaf(child)
        else:
            tree = child
        
        return tree
        
    def __expr2(self):
        """
        Returns
        -------
        ParseTree(ParseType.ADD) or ParseTree(ParseType.SUB)

        """
        tree = None
        
        if self.__has(Token.PLUS) or self.__has(Token.MINUS):
            parse_type = ParseType.ADD if self.__has(Token.PLUS) else ParseType.SUB
            tree = ParseTree(parse_type, self.__lexer.get_tok())
            
            self.__next()
            child = self.__term()  
            tree.children_append_right(child)

            expr_root = self.__expr2()
            
            if expr_root:
                expr_root.insert_left_leaf(tree)
                tree = expr_root       
            
            
        return tree
        
    def __term(self):
        """
        Returns
        -------
        ParseTree(ParseType.DIV) or ParseTree(ParseType.MUL)

        """
        child = self.__factor()
        tree = self.__term2()
        
        if tree:
            tree.insert_left_leaf(child)
        else:
            tree = child
            
        return tree
        
    def __term2(self):
        """
        Returns
        -------
        ParseTree(ParseType.DIV) or ParseTree(ParseType.MUL)

        """
        tree = None
        
        if self.__has(Token.TIMES) or self.__has(Token.DIVISION) or self.__has(Token.MOD):
            if self.__has(Token.TIMES):
                parse_type = ParseType.MUL     
            elif self.__has(Token.DIVISION):
                parse_type = ParseType.DIV
            else:
                parse_type = ParseType.MOD
                
            tree = ParseTree(parse_type, self.__lexer.get_tok())
            
            self.__next()
            child = self.__factor()
            tree.children_append_right(child)
            
            term_root = self.__term2()
            if term_root:
                term_root.insert_left_leaf(tree)
                tree = term_root
            
        return tree

    
    def __factor(self):
        neg=None
        if self.__has(Token.MINUS): 
            neg = ParseTree(ParseType.NEG)
            self.__next()
            
        child = self.__exponent()
        tree = self.__factor2()
        if tree:
            tree.children_append_left(child)
        else:
            tree = child
            
        if neg:
            neg.children_append_left(tree)
            tree = neg
            
        return tree
        
    def __factor2(self):
        """
        Returns
        -------
        ParseTree(ParseType.POW)

        """
        
        tree = None
        if self.__has(Token.POWER):
            tree = ParseTree(ParseType.POW, self.__lexer.get_tok())

            self.__next()
            child = self.__factor()
            tree.children_append_right(child)
        
        return tree
        
    def __exponent(self):
        """
        Returns
        -------
        ParseTree(ParseType)

        """
        tree = None
        if self.__has(Token.LPAREN):
            self.__next()
            tree = self.__expr()
            self.__must_be(Token.RPAREN)
            self.__next()
        elif self.__has(Token.IDENTIFIER):
            tree = self.__ref_or_call_or_pop()
        elif self.__has(Token.NUMBER):
            tree = ParseTree(ParseType.ATOMIC, self.__lexer.get_tok())
            self.__next()
        elif self.__has(Token.STRING):
            tree = ParseTree(ParseType.ATOMIC, self.__lexer.get_tok())
            self.__next()
        elif self.__has(Token.LEN):
            tree = ParseTree(ParseType.LEN, self.__lexer.get_tok())
            
            self.__next()
            self.__must_be(Token.LPAREN)
            
            self.__next()
            self.__must_be(Token.IDENTIFIER)
            child = ParseTree(ParseType.ATOMIC, self.__lexer.get_tok())
            tree.children_append_left(child)
            
            self.__next()
            self.__must_be(Token.RPAREN)
            self.__next()
            
        return tree
            
    def __ref_or_call_or_pop(self):
        """
        Returns
        -------
        ParseTree

        """
        self.__must_be(Token.IDENTIFIER)
        ref = self.__lexer.get_tok()
        tree = ParseTree(ParseType.ATOMIC, ref)
        
        self.__next()
    
        if self.__has(Token.LBRACKET):
            self.__next()
            
            ref_leaf = tree
            loc_leaf = self.__expr()
            tree = ParseTree(ParseType.INDEXING, self.__lexer.get_tok())
            tree.children_extend_right([ref_leaf, loc_leaf])
            
            self.__must_be(Token.RBRACKET)
            self.__next()
        elif self.__has(Token.LPAREN):
            self.__next()
            
            ref_leaf = tree
            tree = ParseTree(ParseType.CALL, self.__lexer.get_tok())
            tree.children_append_left(ref_leaf)
            tree.children_extend_right(self.__call2())   
        
        elif self.__has(Token.DOT):
            self.__next()
            
            self.__must_be(Token.POP)
            ref_leaf = tree
            tree = ParseTree(ParseType.POP, self.__lexer.get_tok())
            tree.children_append_left(ref_leaf)
            
            self.__next()
            self.__must_be(Token.LPAREN)
            
            self.__next()
            self.__must_be(Token.RPAREN)
            
            self.__next()
            
            
        return tree
              
            
    def __call2(self):
        """
        Returns
        -------
        ParseTree[]

        """
        trees = []
        if self.__has(Token.RPAREN):
            self.__next()
        else:
            trees = self.__arg_list()
            self.__must_be(Token.RPAREN)
            self.__next()
            
        return trees
        
    def __input(self):
        """
        Pre: The next token has been consumed and must be for
        Post: Consume the next token before leaving this function
        
        Returns
        -------
        ParseTree(ParseType.INPUT)
        """
        self.__must_be(Token.INPUT)
        tree = ParseTree(ParseType.INPUT, self.__lexer.get_tok())
        
        self.__next()
        tree.children_extend_right(self.__input2())
        
        return tree
        
    def __input2(self):
        """
        Returns
        -------
        ParseTree []

        """
        trees = []
        if self.__has(Token.STRING):
            trees.append(ParseTree(ParseType.ATOMIC, self.__lexer.get_tok()))
            
            self.__next()
            self.__must_be(Token.SEMICOLON)
            self.__next()
       
        trees.extend(self.__ref_list())
        
        return trees
        
    def __ref_list(self):
        """
        Returns
        -------
        ParseTree []

        """
        trees = []
        
        trees.append(self.__ref())
        
        while self.__has(Token.COMMA):
            self.__next()
            trees.append(self.__ref())
            
        return trees
        
        
    def __print(self):
        self.__must_be(Token.PRINT)
        tree = ParseTree(ParseType.PRINT, self.__lexer.get_tok())
        
        self.__next()
        tree.children_extend_right(self.__arg_list())
        
        return tree
        
    
    def __println(self):
        self.__must_be(Token.PRINTLN)
        tree = ParseTree(ParseType.PRINTLN, self.__lexer.get_tok())
        
        self.__next()
        tree.children_extend_right(self.__arg_list())
        
        return tree
        
    def __arg_list(self):
        """
        Returns
        -------
        ParseTree[]

        """
        trees = []
        trees.append(self.__expr())
        
        while self.__has(Token.COMMA):
            self.__next()
            trees.append(self.__expr())
            
        return trees
            
            
            
# unit test 
if __name__ == "__main__":
    if len(sys.argv) == 2:
        f = open(sys.argv[1])
        l = HappyLexer(f)
    else:
        l = HappyLexer()

    p = HappyParser(l)
    tree = p.parse()
    tree.print_tree()

        
            
    
            
        
    
    
    
        