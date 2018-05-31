# -----------------------------------------------------------------------------
# calc.py
#
# p[1] simple calculator with variables.
# -----------------------------------------------------------------------------

tokens = (
    'NAME', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN', 'SEMICOLON', 'EQUALITY', 'NON_EQUALITY', "AND", "OR", "STRING", 'IF', 'LACCO', 'RACCO')
# Tokens
t_LACCO = r"}"
t_RACCO = r"{"
t_IF = r'if'
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
t_NAME = r'((?!(if))([a-zA-Z_][a-zA-Z0-9_]*))'
t_SEMICOLON = ";"
t_STRING = "'[^']*'"


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


def p_bloc(p):
    '''bloc : statement bloc
            | statement'''
    if len(p) == 3:
        p[0] = ('bloc', p[1], p[2])
    else:
        p[0] = ('bloc', p[1], 'empty')
    eval(p[0])


def condition_statement(p):
    '''statement : IF expression'''
    print("tkt")


def p_statement_assign(p):
    '''statement : NAME EQUALS expression SEMICOLON'''
    p[0] = ('=', p[1], p[3])


def p_statement_expr(p):
    '''statement : expression SEMICOLON'''
    p[0] = p[1]
    print(p[0])


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQUALITY expression
                  | expression NON_EQUALITY expression
                  | expression OR expression
                  | expression AND expression '''
    if p[2] == '+':
        p[0] = ('+', p[1], p[3])
    elif p[2] == '-':
        p[0] = ('-', p[1], p[3])
    elif p[2] == '*':
        p[0] = ('*', p[1], p[3])
    elif p[2] == '/':
        p[0] = ('/', p[1], p[3])
    elif p[2] == '==':
        p[0] = ('==', p[1], p[3])
    elif p[2] == '!=':
        p[0] = ('!=', p[1], p[3])
    elif p[2] == '||':
        p[0] = ('||', p[1], p[3])
    elif p[2] == '&&':
        p[0] = ('&&', p[1], p[3])


def eval(p):
    if p == 'empty':
        return
    if p[0] == 'bloc':
        print(eval(p[1]))
        print(eval(p[2]))

    elif p[0] == '+':
        return p[1] + p[2]
    elif p[0] == '-':
        return p[1] - p[2]
    elif p[0] == '*':
        return p[1] * p[2]
    elif p[0] == '/':
        return p[1] / p[2]
    elif p[0] == '==':
        return p[1] == p[2]
    elif p[0] == '!=':
        return p[1] != p[2]
    elif p[0] == '=':
        names[p[1]] = p[2]
    elif p[0] == '||':
        return p[1] or p[2]
    elif p[0] == '&&':
        return p[1] and p[2]


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
    'expression : STRING'
    p[0] = p[1]


def p_expression_name(p):
    'expression : NAME'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_error(p):
    print("Syntax error at '%s'" % p.value)


import ply.yacc as yacc

yacc.yacc()

while True:
    try:
        s = input('calc > ')  # use input() on Python 3
    except EOFError:
        break
    yacc.parse(s)
