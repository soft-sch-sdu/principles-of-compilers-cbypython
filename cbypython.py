import argparse
import sys

from lexer import *


###############################################################################
#                                                                             #
#  DRIVER          - by leon                                                      #
#                                                                             #
###############################################################################


def main():
    parser = argparse.ArgumentParser(
        description='cbypython - Simple C Compiler'
    )
    parser.add_argument('input', help='C source file')

    args = parser.parse_args()
    
    p = args.input
    
    lexer = Lexer(p)
    t = lexer.get_next_token()
    print(f"  .globl main")
    print(f"main:")
    print(f"  mov ${t.value}, %rax")
    t = lexer.get_next_token()
    while t.type != TokenType.TK_EOF:
        if t.type == TokenType.TK_PLUS:
            t = lexer.get_next_token()
            print(f"  add ${t.value}, %rax")
            t = lexer.get_next_token()
            continue
        elif t.type == TokenType.TK_MINUS:
            t = lexer.get_next_token()
            print(f"  sub ${t.value}, %rax")
            t = lexer.get_next_token()
            continue

    print(f"  ret")

if __name__ == '__main__':
    main()
