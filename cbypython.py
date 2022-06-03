import argparse
import sys

from lexer import *
from parser import *
from codegenerator import *


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
    # p = '- (- (+10))'
    lexer = Lexer(p)
    # print(lexer.get_next_token().value)
    # print(lexer.get_next_token().value)
    # print(lexer.get_next_token().value)
    try:
        parser = Parser(lexer)
        tree = parser.parse()
    except (LexerError, ParserError) as e:
        print(e.message)
        sys.exit(1)

    codegenerator= Codegenerator(tree)
    codegenerator.codegenerate()

if __name__ == '__main__':
    main()
