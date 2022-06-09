import argparse
import sys

from lexer import *
from parser import *
from codegenerator import *
from semanticanalyzer import *


class ErrorCode(Enum):
    UNEXPECTED_TOKEN = 'Unexpected token'

class Error(Exception):
    def __init__(self, error_code=None, token=None, message=None):
        self.error_code = error_code
        self.token = token
        # add exception class name before the message
        self.message = f'{self.__class__.__name__}: {message}'


class LexerError(Error):
    pass


class ParserError(Error):
    pass


class SemanticError(Error):
    pass

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

    # lexer.print_all_tokens()

    parser = Parser(lexer)
    tree = parser.parse()

    semantic_analyzer = SemanticAnalyzer(tree)
    symbol_table, offset = semantic_analyzer.semantic_analyze()

    code_generator= Codegenerator(tree, symbol_table, offset)
    code_generator.code_generate()

if __name__ == '__main__':
    main()
