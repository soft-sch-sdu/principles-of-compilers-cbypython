###############################################################################
#                                                                             #
#  LEXER                                                                     #
#                                                                                #
###############################################################################
import string
from enum import Enum
import sys


class TokenType(Enum):
    # single-character token types
    TK_PLUS          = '+'
    TK_MINUS         = '-'
    TK_MUL           = '*'
    TK_DIV           = '/'
    TK_NEG           = 'unary-'
    TK_LT            = '<'
    TK_GT            = '>'
    TK_EQ            = '=='
    TK_NE            = '!='
    TK_GE            = '>='
    TK_LE            = '<='
    TK_LPAREN        = '('
    TK_RPAREN        = ')'
    TK_LBRACE        = '{'
    TK_RBRACE        = '}'
    TK_LBRACK        = '['
    TK_RBRACK        = ']'
    TK_SEMICOLON     = ';'
    # block of reserved words
    TK_RETURN        = 'return'
    # misc
    TK_IDENT         = 'IDENT'
    TK_INTEGER_CONST = 'INTEGER_CONST'
    TK_ASSIGN        = '='
    TK_EOF           = 'EOF'

    @classmethod
    def members(cls):
        return cls._value2member_map_

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Lexer:
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]
        # # list of tokens
        # self.tokens = []

    def verror_at(self, error_list='some error'):
        print(f"{self.text}", file=sys.stderr)
        print("%{pos}s".format(pos=self.pos+1) % "^", end=' ', file=sys.stderr)
        print(f"{error_list}", file=sys.stderr)
        sys.exit(1)


    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # Returns true if c is valid as the first character of an identifier.
    def _is_ident1(self, c):
        return ('a' <= c and c <= 'z') or ('A' <= c and c <= 'Z') or c == '_'
    # Returns true if c is valid as a non-first character of an identifier.
    def _is_ident2(self, c):
        return self._is_ident1(c) or ('0' <= c and c <= '9')

    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""

        # Create a new token
        token = Token(type=None, value=None)

        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        token.type = TokenType.TK_INTEGER_CONST
        token.value = int(result)
        return token


    # Read a punctuator token from p and returns
    def read_punct(self, p):
        if p.startswith("==", self.pos) or \
            p.startswith("!=", self.pos) or \
            p.startswith("<=", self.pos) or \
            p.startswith(">=", self.pos):
            return 2
        return self.current_char in string.punctuation

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:
            # Skip whitespace characters
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Numeric literal
            if self.current_char.isdigit():
                return self.number()

            # Identifier(Beginning with a - z or A - Z or _, not digits, not punctutors other than _)
            if (self._is_ident1(self.current_char)):
                result = self.current_char
                self.advance()
                while (self._is_ident2(self.current_char)):
                    result += self.current_char
                    self.advance()
                # if keyword, not common identifier
                if result in TokenType.members():
                    # get enum member by value, e.g.
                    token_type = TokenType(result)
                    # create a token
                    token = Token(
                        type=token_type,
                        value=token_type.value,  # e.g. 'return', etc
                    )
                    return token
                # if not keyword, but identifier
                else:
                    token = Token(
                        type=TokenType.TK_IDENT,
                        value=result
                    )
                    return token

            # Punctuators
            # two-characters punctuator
            if self.read_punct(self.text) == 2:
                token_type = TokenType(self.text[self.pos:self.pos+2])
                # create a token with two-characters lexeme as its value
                token = Token(
                    type=token_type,
                    value=token_type.value,  # e.g. '!=', '==', etc
                )
                self.advance()
                self.advance()
                return token
            # single-character punctuator
            elif self.current_char in TokenType.members():
               # get enum member by value, e.g.
                # TokenType('+') --> TokenType.PLUS
                token_type = TokenType(self.current_char)
                # create a token with a single-character lexeme as its value
                token = Token(
                    type=token_type,
                    value=token_type.value,  # e.g. '+', '-', etc
                )
                self.advance()
                return token
            # no enum member with value equal to self.current_char
            else:
                self.verror_at("invalid token")

        # EOF (end-of-file) token indicates that there is no more
        # input left for lexical analysis
        return Token(type=TokenType.TK_EOF, value=None)


    def print_all_tokens(self):
        token = self.get_next_token()
        while token.type != TokenType.TK_EOF:
            print(token.value)
            token = self.get_next_token()
        # sys.exit(0)