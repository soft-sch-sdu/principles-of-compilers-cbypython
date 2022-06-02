from lexer import *
###############################################################################
#                                                                             #
#   AST_Node type
#   ND_ADD,     : +
#   ND_SUB,     : -
#   ND_MUL,     : *
#   ND_DIV,     : /
#   ND_NUM,     : num
#   ND_EXPR,    : Expression
#                                                                             #
###############################################################################


class AST:
    pass


class BinOp_Node(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num_Node(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value



###############################################################################
#                                                                             #
#  AST visitors (walkers)                                                     #
#                                                                             #
###############################################################################

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                                #
###############################################################################

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

    def get_next_token(self):
        return self.lexer.get_next_token()

    def error(self, error_code, token):
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token,
            )

    # primary = num | "(" expr ")"
    def primary(self):
        token = self.current_token
        if token.type == TokenType.TK_INTEGER_CONST:
            self.eat(TokenType.TK_INTEGER_CONST)
            return Num_Node(token)
        elif token.type == TokenType.TK_LPAREN:
            self.eat(TokenType.TK_LPAREN)
            node = self.expression()
            self.eat(TokenType.TK_RPAREN)
            return node

    # mul = primary ("*" primary | "/" primary)*
    def multiplication(self):
        node = self.primary()
        while True:
            token = self.current_token
            if self.current_token.type == TokenType.TK_MUL:
                self.eat(TokenType.TK_MUL)
                node = BinOp_Node(left=node, op=token, right=self.primary())
                continue
            if self.current_token.type == TokenType.TK_DIV:
                self.eat(TokenType.TK_DIV)
                node = BinOp_Node(left=node, op=token, right=self.primary())
                continue
            return node

    # expr = mul ("+" mul | "-" mul)*
    def expression(self):
        node = self.multiplication()
        while True:
            token = self.current_token
            if self.current_token.type == TokenType.TK_PLUS:
                self.eat(TokenType.TK_PLUS)
                node = BinOp_Node(left=node, op=token, right=self.multiplication())
                continue
            if self.current_token.type == TokenType.TK_MINUS:
                self.eat(TokenType.TK_MINUS)
                node = BinOp_Node(left=node, op=token, right=self.multiplication())
                continue
            return node

    def parse(self):
        """
        expr = mul ("+" mul | "-" mul)*
        mul = primary ("*" primary | "/" primary)*
        primary = num | "(" expr ")"
        """
        node = self.expression()
        if self.current_token.type != TokenType.TK_EOF:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token,
            )
        return node
