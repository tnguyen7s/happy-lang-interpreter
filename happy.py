# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 07:23:27 2022

@author: Tuyen
"""

from happylang_parser import ParseType, HappyParser
from happylang_lexer import HappyLexer, Token, TokenDetail
import sys

def eval_parse_tree(t):
    """
    Evaluate the given parse tree

    Parameters
    ----------
    t : ParseTree
    """
    if t.parse_type == ParseType.PROGRAM:
        return eval_PROGRAM(t)
    elif t.parse_type == ParseType.FUN:
        return 
    elif t.parse_type == ParseType.BLOCK:
        return eval_BLOCK(t)
    elif t.parse_type == ParseType.ATOMIC:
        return eval_ATOMIC(t)
    elif t.parse_type == ParseType.ADD:
        return eval_ADD(t)
    elif t.parse_type == ParseType.SUB:
        return eval_SUB(t)
    elif t.parse_type == ParseType.MUL:
        return eval_MUL(t)
    elif t.parse_type == ParseType.DIV:
        return eval_DIV(t)
    elif t.parse_type == ParseType.POW:
        return eval_POW(t)
    elif t.parse_type == ParseType.NEG:
        return eval_NEG(t)
    elif t.parse_type == ParseType.LEN:
        return
    elif t.parse_type == ParseType.INDEXING:
        return
    elif t.parse_type == ParseType.CALL:
        return
    elif t.parse_type == ParseType.VAR:
        return
    elif t.parse_type == ParseType.VAR_AR:
        return
    elif t.parse_type == ParseType.VAR_STK:
        return
    elif t.parse_type == ParseType.ASSIGN:
        return
    elif t.parse_type == ParseType.SWAP:
        return
    elif t.parse_type == ParseType.PUSH:
        return
    elif t.parse_type == ParseType.POP:
        return
    elif t.parse_type == ParseType.IF:
        return eval_IF(t)
    elif t.parse_type == ParseType.IFELSE:
        return eval_IFELSE(t)
    elif t.parse_type == ParseType.AND:
        return eval_AND(t)
    elif t.parse_type == ParseType.OR:
        return eval_OR(t)
    elif t.parse_type == ParseType.EQ:
        return eval_EQ(t)
    elif t.parse_type == ParseType.NE:
        return eval_NE(t)
    elif t.parse_type == ParseType.LT:
        return eval_LT(t)
    elif t.parse_type == ParseType.LE:
        return eval_LE(t)
    elif t.parse_type == ParseType.GT:
        return eval_GT(t)
    elif t.parse_type == ParseType.GE:
        return eval_GE(t)
    elif t.parse_type == ParseType.LOOP:
        return eval_LOOP(t)
    elif t.parse_type == ParseType.PRINT:
        return eval_PRINT(t)
    elif t.parse_type == ParseType.PRINTLN:
        return eval_PRINTLN(t)
    elif t.parse_type == ParseType.INPUT:
        return 
    
def eval_PROGRAM(t):
    return eval_parse_tree(t.children[0])

def eval_BLOCK(t):
    for stmt in t.children:
        eval_parse_tree(stmt)
        
def eval_ATOMIC(t):
    if t.token_detail.token in [Token.STRING, Token.NUMBER]:
        return t.token_detail.value

    
def eval_ADD(t):
    left = eval_parse_tree(t.children[0])
    right = eval_parse_tree(t.children[1])
    
    return left + right

def eval_SUB(t):
    left = eval_parse_tree(t.children[0])
    right = eval_parse_tree(t.children[1])

    return left - right

def eval_MUL(t):
    left = eval_parse_tree(t.children[0])
    right = eval_parse_tree(t.children[1])
    
    return left*right

def eval_DIV(t):
    left = eval_parse_tree(t.children[0])
    right = eval_parse_tree(t.children[1])
    
    if right==0:
        print(f"Division by 0 on line {t.token_detail.line}")
        sys.exit(-1)
    
    return left/right

def eval_POW(t):
    left = eval_parse_tree(t.children[0])
    right = eval_parse_tree(t.children[1])

    return left**right

def eval_NEG(t):
    return -eval_parse_tree(t.children[0])
    

def eval_PRINT(t):
    string = ""
    
    for arg in t.children:
        string += str(eval_parse_tree(arg)) + " "
        
    print(string, end="")
    
def eval_PRINTLN(t):
    string = ""
    
    for arg in t.children:
        string += str(eval_parse_tree(arg)) + " "
        
    print(string)
    
def eval_IF(t):
    cond = t.children[0]
    b = t.children[1]
    
    if eval_parse_tree(cond):
        return eval_parse_tree(b)

def eval_IFELSE(t):
    cond = t.children[0]
    b1 = t.children[1]
    b2 = t.children[2]
    
    if eval_parse_tree(cond):
        return eval_parse_tree(b1)
    else:
        return eval_parse_tree(b2)

def eval_AND(t):
    left = eval_parse_tree(t.children[0])
    right = eval_parse_tree(t.children[1])
    
    return left and right

def eval_OR(t):
    left = eval_parse_tree(t.children[0])
    right = eval_parse_tree(t.children[1])
    
    return left or right

def eval_EQ(t):
    left = eval_parse_tree(t.children[0])
    right = eval_parse_tree(t.children[1])
    
    return left==right

def eval_NE(t):
    left = eval_parse_tree(t.children[0])
    right = eval_parse_tree(t.children[1])
    
    return left!=right

def eval_GE(t):
    left = eval_parse_tree(t.children[0])
    right = eval_parse_tree(t.children[1])
    
    return left>=right

def eval_GT(t):
    left = eval_parse_tree(t.children[0])
    right = eval_parse_tree(t.children[1])
    
    return left>right

def eval_LE(t):
    left = eval_parse_tree(t.children[0])
    right = eval_parse_tree(t.children[1])
    
    return left<=right

def eval_LT(t):
    left = eval_parse_tree(t.children[0])
    right = eval_parse_tree(t.children[1])
    
    return left<right

def eval_LOOP(t):
    pass
    
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        f = open(sys.argv[1])
        l = HappyLexer(f)
    else:
        l = HappyLexer()
        
    parser = HappyParser(l)
    pt = parser.parse()
    pt.print_tree()
    eval_parse_tree(pt)