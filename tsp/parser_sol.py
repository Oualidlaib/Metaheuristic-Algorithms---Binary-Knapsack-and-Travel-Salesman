import ply.yacc as yacc
from tsp.lexer_sol import tokens
 
def p_file(p):
    """file : entry_list"""
    p[0] = p[1]
 
 
def p_entry_list_multiple(p):
    """entry_list : entry_list entry"""
    p[1].update(p[2])
    p[0] = p[1]
 
 
def p_entry_list_single(p):
    """entry_list : entry"""
    p[0] = p[1]
 
 
def p_entry(p):
    """entry : INSTANCE_NAME COLON NUMBER"""
    p[0] = {p[1]: p[3]}
 
parser = yacc.yacc()