# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 07:23:27 2022

@author: Tuyen
"""

from happylang_parser import ParseType, HappyParser, RefType
from happylang_lexer import HappyLexer, Token, TokenDetail
import sys
from collections import ChainMap

"""
Outer reference  environments consist of functions
Inner reference environments consist of variables, stacks, and arrays
"""


class Ref:
    def __init__(self, ref_type, ref_tree, val=None):
        """        

        Parameters
        ----------
        ref_type : RefType
        ref_tree: Parse Tree
        val : Value of the reference

        """
        self.ref_type = ref_type
        self.ref_tree = ref_tree
        self.val = val


class RefEnv:
    def __init__(self, parent=None):
        self.parent = parent
        self.table = ChainMap()

        if parent:
            self.table = ChainMap(self.table, parent.table)

    def lookup(self, ref_name):
        """
        Looks up the value of the reference from the env, from the inner most to the outer most

        Parameters
        ----------
        r : Ref name

        Returns
        -------
        ParseTree

        """

        if ref_name in self.table:
            return self.table[ref_name]

        return None

    def insert(self, ref_name, ref):
        """
        Insert the reference into the inner most env

        Parameters
        ----------
        ref_name: the string name of the reference
        ref: Ref
        """
        self.table[ref_name] = ref


def eval_parse_tree(t, env):
    """
    Evaluate the given parse tree

    Parameters
    ----------
    t : ParseTree
    """
    if t.parse_type == ParseType.PROGRAM:
        return eval_PROGRAM(t, env)
    elif t.parse_type == ParseType.FUN:
        return eval_FUN(t, env)
    elif t.parse_type == ParseType.MAIN:
        return eval_MAIN(t, env)
    elif t.parse_type == ParseType.VAR:
        return eval_VAR(t, env)
    elif t.parse_type == ParseType.BLOCK:
        return eval_BLOCK(t, env)
    elif t.parse_type == ParseType.ATOMIC:
        return eval_ATOMIC(t, env)
    elif t.parse_type == ParseType.ADD:
        return eval_ADD(t, env)
    elif t.parse_type == ParseType.SUB:
        return eval_SUB(t, env)
    elif t.parse_type == ParseType.MUL:
        return eval_MUL(t, env)
    elif t.parse_type == ParseType.DIV:
        return eval_DIV(t, env)
    elif t.parse_type == ParseType.POW:
        return eval_POW(t, env)
    elif t.parse_type == ParseType.NEG:
        return eval_NEG(t, env)
    elif t.parse_type == ParseType.LEN:
        return eval_LEN(t, env)
    elif t.parse_type == ParseType.INDEXING:
        return eval_INDEXING(t, env)
    elif t.parse_type == ParseType.CALL:
        return eval_CALL(t, env)
    elif t.parse_type == ParseType.ASSIGN:
        return eval_ASSIGN(t, env)
    elif t.parse_type == ParseType.SWAP:
        return eval_SWAP(t, env)
    elif t.parse_type == ParseType.PUSH:
        return eval_PUSH(t, env)
    elif t.parse_type == ParseType.POP:
        return eval_POP(t, env)
    elif t.parse_type == ParseType.IF:
        return eval_IF(t, env)
    elif t.parse_type == ParseType.IFELSE:
        return eval_IFELSE(t, env)
    elif t.parse_type == ParseType.AND:
        return eval_AND(t, env)
    elif t.parse_type == ParseType.OR:
        return eval_OR(t, env)
    elif t.parse_type == ParseType.EQ:
        return eval_EQ(t, env)
    elif t.parse_type == ParseType.NE:
        return eval_NE(t, env)
    elif t.parse_type == ParseType.LT:
        return eval_LT(t, env)
    elif t.parse_type == ParseType.LE:
        return eval_LE(t, env)
    elif t.parse_type == ParseType.GT:
        return eval_GT(t, env)
    elif t.parse_type == ParseType.GE:
        return eval_GE(t, env)
    elif t.parse_type == ParseType.LOOP:
        return eval_LOOP(t, env)
    elif t.parse_type == ParseType.PRINT:
        return eval_PRINT(t, env)
    elif t.parse_type == ParseType.PRINTLN:
        return eval_PRINTLN(t, env)
    elif t.parse_type == ParseType.INPUT:
        return eval_INPUT(t, env)


def eval_PROGRAM(t, env):
    """
    Program contains many functions

    called function will be located below the calling function, thus eval the called functions first
    """
    for FUN_parse_tree in t.children[-1:0:-1]:
        eval_parse_tree(FUN_parse_tree, env)

    # here, evaluating main
    eval_parse_tree(t.children[0], env)


def eval_MAIN(t, env):
    """
    eval main block
    """
    main_env = RefEnv(env)
    eval_parse_tree(t.children[0], main_env)


def eval_FUN(t, env):
    """
    store the ref to the function ready to be used
    """
    fun_name = t.token_detail.lexeme

    if env.lookup(fun_name):
        print(f"Function defined twice on line {t.token_detail.line}")
        sys.exit(-1)

    env.insert(fun_name, Ref(RefType.FUN, t))


def eval_CALL(t, env):
    fun_name = t.children[0].token_detail.lexeme
    fun_args = t.children[1:]

    # check the existence of the function
    fun_ref = env.lookup(fun_name)
    if not fun_ref:
        print(f"Undefined function is called on line {t.token_detail.line}")
        sys.exit(-1)
        
    if fun_ref.ref_type != RefType.FUN:
        print(f"Non function is called on line {t.token_detail.line}")
        sys.exit(-1)
        
    fun_tree = fun_ref.ref_tree

    # if fun does exist
    # obtain the definition of function parameters
    param_trees = fun_tree.children[:-1:1]
    if len(fun_args) != len(param_trees):
        print(
            f"Number of arguments does not MATCH number of function's parameters on line {t.token_detail.line}")
        sys.exit(-1)

    called_fun_env = RefEnv(env.parent)
    for i, param in enumerate(param_trees):
        # parameter
        param_data_type = param.children[0].token_detail.lexeme
        param_ref_type = param.ref_type
        param_name = param.children[1].token_detail.lexeme
        
        # argument
        arg = eval_parse_tree(fun_args[i], env)
        
        arg_ref_type = None
        arg_data_type = None
        arg_value = None
        if type(arg)==str:
            arg_ref_type = RefType.PRIMITIVE
            arg_data_type = "STRING"
            arg_value = arg
        elif type(arg)==float:
            arg_ref_type = RefType.PRIMITIVE
            arg_data_type = "NUMBER"
            arg_value = arg
        else:
            arg_ref_type = arg.ref_type
            arg_data_type = arg.ref_tree.children[0].token_detail.lexeme
            arg_value = arg.val
            
        
        # check param and arg
        if param_data_type != arg_data_type or param_ref_type != arg_ref_type:
            print(
                f"Data Type not matched on line {t.token_detail.line}, column {param.children[1].token_detail.col}.\nExpect {param_data_type+' '+param_ref_type.name}, but received {arg_data_type+' '+arg_ref_type.name}")
            sys.exit(-1)

        # bind the variable to the enviroment
        called_fun_env.insert(param_name, Ref(
            param_ref_type, param_trees[i], arg_value))

    # eval the fun's block
    eval_parse_tree(fun_tree.children[-1], called_fun_env)


def eval_BLOCK(t, env):
    """
    eval stmt and var-decl
    """
    for stmt in t.children:
        eval_parse_tree(stmt, env)

def default_number():
    return float(0)

def eval_VAR(t, env):
    """
    stored declared variables inside the local env
    """
    var_name = t.children[1].token_detail.lexeme

    if env.lookup(var_name):
        print(f"Reference declared twice on line {t.token_detail.line}")
        sys.exit(-1)
    
    val = default_number()
    if t.ref_type == RefType.PRIMITIVE and t.children[0].token_detail.token==Token.STRING_TP:
        val=""
    
    if t.ref_type == RefType.ARRAY:
        length = eval_parse_tree(t.children[-1], env)
        val = [default_number()]*int(length)
        
    if t.ref_type == RefType.STACK:
        val = []
     
    env.insert(var_name, Ref(t.ref_type, t, val))


def eval_ATOMIC(t, env):
    """
    return value for primitive data type
    otherwise Ref
    """
    if t.token_detail.token in [Token.STRING, Token.NUMBER]:
        return t.token_detail.value
    
    identifier = t.token_detail.lexeme
    var_ref = env.lookup(identifier)
    if not var_ref:
        print(f"Undefined variable {identifier} on line {t.token_detail.line}")
        sys.exit(-1)
        
    if var_ref.ref_type == RefType.PRIMITIVE:
        return var_ref.val

    return var_ref

def eval_INPUT(t, env):
    refs = t.children
    
    if refs[0].token_detail.token==Token.STRING:
        print(refs[0].token_detail.lexeme)
        refs = refs[1:]
        
    for r in refs:
        # get the ref object of the variable
        var_ref, idx = eval_REF(r, env)
        
        # read the input
        input_val = input()
        if var_ref.ref_tree.children[0].token_detail.lexeme=="NUMBER":
            input_val = float(input_val)
        
        # assign the input value to the Ref object
        if idx==-1:
            var_ref.val = input_val
        else:
            
            if idx>=len(var_ref.val):
                print(f"Index out of range on line {t.token_detail.line}")
                print(f"List of size {len(var_ref.val)}")
                sys.exit(-1)
            
            var_ref.val[idx] = input_val
        
        

def eval_INDEXING(t, env):
    a = eval_parse_tree(t.children[0], env)
        
    if type(a)!=Ref or a.ref_type not in [RefType.ARRAY, RefType.STACK]:
        print(f"Indexing only applies to ARRAY or STACK, on line {t.token_detail.line}")
        sys.exit(-1)
        
    seq = a.val
    
    index = int(eval_parse_tree(t.children[1], env))
    if index>=len(seq):
        print(f"Index out of range on line {t.token_detail.line}")
        sys.exit(-1)
        
    return seq[index]

def eval_PUSH(t, env):
    var_ref = eval_VAR_REF(t.children[0], env)
    
    if var_ref.ref_type != RefType.STACK:
        print(f"Expect a stack on line {t.token_detail.line}")
        sys.exit(-1)
    
    pushed_value = eval_parse_tree(t.children[1], env)
    
    stack_data_type = var_ref.ref_tree.children[0].token_detail.lexeme
    if (type(pushed_value)==str and stack_data_type!="STRING") or (type(pushed_value)==float and stack_data_type!="NUMBER"):
        print(f"On line {t.token_detail.line}, stack is of type {stack_data_type}, but the pushed value is not a {stack_data_type}")
        sys.exit(-1)
        
    var_ref.val.append(pushed_value)
    
    return pushed_value
    

def eval_POP(t, env):
    var_ref = eval_VAR_REF(t.children[0], env)
    
    if var_ref.ref_type != RefType.STACK:
        print(f"Expect a stack on line {t.token_detail.line}")
        sys.exit(-1)
    
    popped_val = var_ref.val[-1]
    del var_ref.val[-1]
    return popped_val


def eval_ASSIGN(t, env):
    var_ref, idx = eval_REF(t.children[0], env)
    val = eval_parse_tree(t.children[1], env)
    
    
    if idx==-1:
        if type(val)!=type(var_ref.val):
            print(f"Unmatched type when do the assignment on line {t.token_detail.line}")
            sys.exit(-1)

        var_ref.val = val
    else:
        if idx>=len(var_ref.val):
            print(f"Index out of range on line {t.token_detail.line}")
            sys.exit(-1)
            
        if type(val)!=type(var_ref.val[idx]):
            print(f"Unmatched type when do the assignment on line {t.token_detail.line}")
            sys.exit(-1)
            
        var_ref.val[idx] = val
        
def eval_SWAP(t, env):
    left_var_ref, left_idx = eval_REF(t.children[0], env)
    right_var_ref, right_idx = eval_REF(t.children[1], env)
    
    left_val = None
    if left_idx==-1:
        left_val = left_var_ref.val
    else:
        if left_idx>=len(left_var_ref.val):
            print(f"Index out of range on line {t.token_detail.line}")
            sys.exit(-1)
        
        left_val = left_var_ref.val[left_idx]
    
    right_val = None
    if right_idx==-1:
        right_val = right_var_ref.val
    else:
        if right_idx>=len(right_var_ref.val):
            print(f"Index out of range on line {t.token_detail.line}")
            sys.exit(-1)
            
        right_val = right_var_ref.val[right_idx]
        
    # check data type
    if type(left_val)!=type(right_val):
        print(f"Unmatched data type when do the swap on line {t.token_detail.line}")
        sys.exit(-1)
    
    # swap
    tmp = left_val
    left_val = right_val
    right_val = tmp
    
    
    # assign value to Refs
    if left_idx==-1:
        left_var_ref.val = left_val
    else:
        left_var_ref.val[left_idx] = left_val
    
    if right_idx==-1:
        right_var_ref.val = right_val
    else:
        right_var_ref.val[right_idx] = right_val
         

def eval_REF(t, env):
    """
    Returns
    -------
    var_ref : Ref
    idx : -1 or the index

    """
    var_ref = None
    idx = None
    if t.parse_type == ParseType.INDEXING:
        var_ref = eval_VAR_REF(t.children[0], env)
        idx = int(eval_parse_tree(t.children[1], env))
    else:
        var_ref = eval_VAR_REF(t, env)
        idx = -1
        
    return (var_ref, idx)

def eval_VAR_REF(t, env):
    """
    var_ref : Ref

    """
    identifier = t.token_detail.lexeme
    var_ref = env.lookup(identifier)
    if not var_ref:
        print(f"Undefined variable {identifier} on line {t.token_detail.line}")
        sys.exit(-1)
        
    if var_ref.ref_type == RefType.FUN:
        print(f"{identifier} is not a variable, on line {t.token_detail.line}")
        sys.exit(-1)
        
    return var_ref

def eval_ADD(t, env):
    left = eval_parse_tree(t.children[0], env)
    right = eval_parse_tree(t.children[1], env)

    return left + right


def eval_SUB(t, env):
    left = eval_parse_tree(t.children[0], env)
    right = eval_parse_tree(t.children[1], env)

    return left - right


def eval_MUL(t, env):
    left = eval_parse_tree(t.children[0], env)
    right = eval_parse_tree(t.children[1], env)

    return left*right


def eval_DIV(t, env):
    left = eval_parse_tree(t.children[0], env)
    right = eval_parse_tree(t.children[1], env)

    if right == 0:
        print(f"Division by 0 on line {t.token_detail.line}")
        sys.exit(-1)

    return left/right


def eval_POW(t, env):
    left = eval_parse_tree(t.children[0], env)
    right = eval_parse_tree(t.children[1], env)

    return left**right


def eval_NEG(t, env):
    return -eval_parse_tree(t.children[0], env)


def eval_PRINT(t, env):
    string = ""

    for arg in t.children:
        val = eval_parse_tree(arg, env)
        if type(val) == float:
            val = str(val)
        
        string += val

    print(string, end="")


def eval_PRINTLN(t, env):
    string = ""

    for arg in t.children:
        val = eval_parse_tree(arg, env)
        if type(val) == float:
            val =str(val)
            
            
        string += val

    print(string)


def eval_IF(t, env):
    cond = t.children[0]
    b = t.children[1]

    if eval_parse_tree(cond, env):
        return eval_parse_tree(b, env)


def eval_IFELSE(t, env):
    cond = t.children[0]
    b1 = t.children[1]
    b2 = t.children[2]

    if eval_parse_tree(cond, env):
        return eval_parse_tree(b1, env)
    else:
        return eval_parse_tree(b2, env)


def eval_AND(t, env):
    left = eval_parse_tree(t.children[0], env)
    right = eval_parse_tree(t.children[1], env)

    return left and right


def eval_OR(t, env):
    left = eval_parse_tree(t.children[0], env)
    right = eval_parse_tree(t.children[1], env)

    return left or right


def eval_EQ(t, env):
    left = eval_parse_tree(t.children[0], env)
    right = eval_parse_tree(t.children[1], env)

    return left == right


def eval_NE(t, env):
    left = eval_parse_tree(t.children[0], env)
    right = eval_parse_tree(t.children[1], env)

    return left != right


def eval_GE(t, env):
    left = eval_parse_tree(t.children[0], env)
    right = eval_parse_tree(t.children[1], env)

    return left >= right


def eval_GT(t, env):
    left = eval_parse_tree(t.children[0], env)
    right = eval_parse_tree(t.children[1], env)

    return left > right


def eval_LE(t, env):
    left = eval_parse_tree(t.children[0], env)
    right = eval_parse_tree(t.children[1], env)

    return left <= right


def eval_LT(t, env):
    left = eval_parse_tree(t.children[0], env)
    right = eval_parse_tree(t.children[1], env)

    return left < right


def eval_LOOP(t, env):
    condition_idx = 0
    
    for i in range(len(t.children)):
        if t.children[i].parse_type in [ParseType.AND, ParseType.OR, ParseType.LT, ParseType.LE, ParseType.GT, ParseType.GE, ParseType.NE, ParseType.EQ]:
            condition_idx = i
            break
        
    condition_tree = t.children[condition_idx]
    start_loop_assign_trees = t.children[:condition_idx]
    loop_assign_trees = t.children[condition_idx+1:-1]
    block = t.children[-1]
    
    # start loop assignments
    for t in start_loop_assign_trees:
        eval_parse_tree(t, env)

    # loop
    while eval_parse_tree(condition_tree, env):
        eval_parse_tree(block, env)
        
        for t in loop_assign_trees:
            eval_parse_tree(t, env)
        

def eval_LEN(t, env):
    v = eval_parse_tree(t.children[0], env)
        
    if type(v)!=Ref or v.ref_type not in [RefType.ARRAY, RefType.STACK]:
        print(f"len() expects argument of type ARRAY or STACK on line {t.token_detail.line}")
        sys.exit(-1)
    
    
    return len(v.val)  

  
if __name__ == "__main__":
    f = None
    if len(sys.argv) == 2:
        f = open(sys.argv[1], encoding="utf8")
        l = HappyLexer(f)
    else:
        l = HappyLexer()

    parser = HappyParser(l)
    pt = parser.parse()
    eval_parse_tree(pt, RefEnv())
    
    if f:
        f.close()
