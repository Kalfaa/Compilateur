# -----------------------------------------------------------------------------
# calc.py
#
# p[1] simple calculator with variables.
# -----------------------------------------------------------------------------

import uuid
import graphviz as gv

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for' : 'FOR',
    'def' : 'DEF',
    'break' : 'BREAK',
    'return' : 'RETURN',
    'print' : 'PRINT'
}
tokens = [  'LESSER','UPPER',
             'NAME', 'NUMBER',
             'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
             'LPAREN', 'RPAREN', 'SEMICOLON', 'EQUALITY', 'NON_EQUALITY', "AND", "OR", "STRING", 'LACCO',
             'RACCO','COMA','QUOTE'] + list(reserved.values())
# Tokens
t_UPPER = r'>'
t_LESSER = r'<'
t_LACCO = r"{"
t_RACCO = r"}"
t_EQUALITY = r'=='
t_NON_EQUALITY = r'!='
t_OR = r'&&'
t_AND = r'\|\|'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = ";"
t_COMA = ','
t_QUOTE ='\"'
t_STRING=r'oo'

# t_NAME = r'((?!(if))([a-zA-Z_][a-zA-Z0-9_]*))'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')  # Check for reserved words
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lex.lex()

# Precedence rules for the arithmetic operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS')
)

# dictionary of names (for storing variables)
names = {}
function = {}
bool_return = [0,None]
function_scope = [0,None]

def printTreeGraph(t):
    graph = gv.Digraph(format='pdf')
    graph.attr('node', shape='circle')
    addNode(graph, t)
    #graph.render(filename='img/graph') #Pour Sauvegarder
    graph.view() #Pour afficher

def addNode(graph, t):
    myId = uuid.uuid4()

    if type(t) != tuple:
        graph.node(str(myId), label=str(t))
        return myId

    graph.node(str(myId), label=str(t[0]))
    graph.edge(str(myId), str(addNode(graph, t[1])), arrowsize='0')
    if len(t) > 2:
        graph.edge(str(myId), str(addNode(graph, t[2])), arrowsize='0')

    return myId

def p_master(p):
    '''master : bloc'''
    print(p[1])
    eval(p[1])
    printTreeGraph(p[1])

def p_bloc(p):
    '''bloc :  statement bloc
            | statement'''
    bool_return[0] = 0
    if len(p) == 3:
        p[0] = ('bloc', p[1], p[2])
    else:
        p[0] = ('bloc', p[1], 'empty')


def p_IF_statement(p):
    '''statement : IF expression LACCO bloc RACCO ELSE LACCO bloc RACCO
    | IF expression  LACCO bloc RACCO   '''
    if len(p) == 6:
        p[0] = (p[1], p[2], p[4])
    else:
        p[0] = (p[1], p[2], p[4], p[8])

    print(p[0])

def p_FOR_statement(p):
    '''statement : FOR statement statement statement LACCO bloc RACCO
                |  FOR statement statement LACCO bloc RACCO'''
    if len(p) == 8:
        p[0] = (p[1], p[3], p[4], p[6], p[2])
    else :
        p[0] = (p[1], p[2], p[3], p[5])
def p_WHILE_statement(p):
    '''statement : WHILE expression  LACCO bloc RACCO '''
    p[0] = (p[1], p[2], p[4])


def p_statement_assign(p):
    '''statement : NAME EQUALS expression SEMICOLON'''
    p[0] = ('=', p[1], p[3])
    print(p[0])


def p_statement_expr(p):
    '''statement : expression SEMICOLON'''
    p[0] = p[1]


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQUALITY expression
                  | expression NON_EQUALITY expression
                  | expression OR expression
                  | expression AND expression
                  | expression UPPER expression
                  | expression LESSER expression'''

    p[0] = (p[2], p[1], p[3])
    print(p[0])

def p_def_function(p):
    '''statement : DEF NAME LPAREN arglist RPAREN LACCO bloc RACCO
                  | DEF NAME LPAREN RPAREN LACCO bloc RACCO'''
    if len(p) == 9:
        p[0] = (p[1],p[2],p[7],p[4])
    else:
        p[0] = (p[1],p[2],p[6])

def p_exec_function(p):
    '''expression : NAME LPAREN RPAREN
                 | NAME LPAREN expressionlist RPAREN'''
    if len(p)== 4:
        p[0]= ('exec', p[1]);
    else :
        p[0] = ('exec', p[1],p[3]);

def eval(p):
        global function_scope
        global function_bloc
        global bool_return
        if type(p) == tuple:
            if bool_return[0] == 1:
                return bool_return[1]
            if p[0] == 'return' :
                bool_return[1] = eval(p[1])
                bool_return[0] = 1
                return 'empty'
            if p == 'empty':
                return
            if p[0] == 'bloc':
               eval(p[1])
               eval(p[2])
            if p[0] == 'exec':
                if len(p) ==3:
                    name_list = function[p[1]][1]
                    value = eval(p[2])
                    i=0
                    names['!' + p[1]] = {}
                    if(len(value)>len(name_list)):
                        raise "TO MUCH ARGUMENT"
                    for i in range(len(name_list)):
                        names['!'+p[1]][name_list[i]] = value[i]

                function_bloc = function[p[1]][0]
                temp = function_scope
                function_scope = [1, p[1]]
                eval(function_bloc)
                function_scope = temp
                bool_return[0] = 0
                return_value = bool_return[1]
                bool_return[1] = None
                return return_value
            if p[0] == "while":
                while type(p[1]) is tuple and eval(p[1]):
                    eval(p[2])
            if p[0] == 'print':
                print(eval(p[1]))
            if p[0] == "if":
                if type(p[1]) is tuple and eval(p[1]):
                    eval(p[2])
                elif len(p) == 4:
                    eval(p[3])
            if p[0] == "for":
                if len(p) == 5:
                    eval(p[4])
                while eval(p[1]):
                    eval(p[3])
                    eval(p[2])
            if p[0] == "arglist":
                if (p[2] == 'empty'):
                    return eval(p[1])

                return eval(p[1])+','+eval(p[2])
            if p[0] == "exprlist":
                if p[2] =='empty':
                    return [eval(p[1])]
                return eval(p[1])+[eval(p[2])]
            if p[0] == "def":
                if len(p) == 4:
                    list_arg = eval(p[3])
                    function[p[1]] =(p[2],list_arg.split(","))
                    return 'empty'
                else:
                    function[p[1]] = (p[2],None)
            if p[0] == '+':
                return eval(p[1]) + eval(p[2])
            elif p[0] == '-':
                return eval(p[1]) - eval(p[2])
            elif p[0] == '*':
                return eval(p[1]) * eval(p[2])
            elif p[0] == '/':
                return eval(p[1]) / eval(p[2])
            elif p[0] == '==':
                return eval(p[1]) == eval(p[2])
            elif p[0] == '!=':
                return eval(p[1]) != eval(p[2])
            elif p[0] == '=':
                if function_scope[0] == 1:
                    names['!' + function_scope[1]][p[1]] = eval(p[2])
                else:
                    names[p[1]] = eval(p[2])
            elif p[0] == '||':
                return eval(p[1]) or eval(p[2])
            elif p[0] == '&&':
                return eval(p[1]) and eval(p[2])
            elif p[0] == 'var':
                try:
                    if function_scope[0] ==1:
                        return names['!'+function_scope[1]][p[1]]
                    return names[p[1]]
                except KeyError as x:
                    print ("UNDEFINED VAR :"+p[1])
            elif p[0] == "<":
                return eval(p[1]) < eval(p[2])
            elif p[0] == ">":
                return eval(p[1]) > eval(p[2])
        else:
            if p == 'return' :
                bool_return[0] = 1
                return
            return p


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_string(p):
    '''expression : QUOTE STRING QUOTE'''
    p[0] = p[2]


def p_expression_name(p):
    'expression : NAME'
    p[0] = ('var',p[1])

def p_return_name(p):
    '''statement : RETURN SEMICOLON
                    | RETURN expression SEMICOLON'''
    if len(p)==4:
        p[0] = (p[1],p[2])
    else:
        p[0] = (p[1])

def p_arg_list(p):
    '''arglist : arglist COMA NAME
                | NAME'''
    if len(p) == 4:
        p[0] = ('arglist', p[1], p[3])
    else:
        p[0] = ('arglist', p[1],'empty')

def p_expression_list(p):
    '''expressionlist : expressionlist COMA expression
                        | expression'''
    if len(p) == 4:
        p[0] = ('exprlist', p[1], p[3])
    else:
        p[0] = ('exprlist', p[1],'empty')

def p_error(p):
    print("Syntax error at '%s'" % p.value)

def p_print(p):
    '''expression : PRINT LPAREN expression RPAREN'''
    p[0] = (p[1],p[3])
import ply.yacc as yacc

yacc.yacc()


with open("code2")as f:
    s = f.read()  # use input() on Python 3

yacc.parse(s)