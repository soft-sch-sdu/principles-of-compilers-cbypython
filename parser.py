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


class UnaryOp_Node(AST):
    def __init__(self, op, right):
        self.token = self.op = op
        self.right = right


class BinaryOp_Node(AST):
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

    #unary = ("+" | "-")? primary
    def unary(self):
        token = self.current_token
        if token.type == TokenType.TK_PLUS:
            self.eat(TokenType.TK_PLUS)
            return UnaryOp_Node(op=token, right=self.primary())
        elif token.type == TokenType.TK_MINUS:
            self.eat(TokenType.TK_MINUS)
            return UnaryOp_Node(op=token, right=self.primary())
        else:
            return self.primary()

    # mul_div = unary ("*" unary | "/" unary)*
    def mul_div(self):
        node = self.unary()
        while True:
            token = self.current_token
            if self.current_token.type == TokenType.TK_MUL:
                self.eat(TokenType.TK_MUL)
                node = BinaryOp_Node(left=node, op=token, right=self.unary())
                continue
            if self.current_token.type == TokenType.TK_DIV:
                self.eat(TokenType.TK_DIV)
                node = BinaryOp_Node(left=node, op=token, right=self.unary())
                continue
            return node

    # add-sub = mul_div ("+" mul_div | "-" mul_div)*
    def add_sub(self):
        node = self.mul_div()
        while True:
            token = self.current_token
            if self.current_token.type == TokenType.TK_PLUS:
                self.eat(TokenType.TK_PLUS)
                node = BinaryOp_Node(left=node, op=token, right=self.mul_div())
                continue
            if self.current_token.type == TokenType.TK_MINUS:
                self.eat(TokenType.TK_MINUS)
                node = BinaryOp_Node(left=node, op=token, right=self.mul_div())
                continue
            return node

    # relational = add_sub ("<" add_sub | "<=" add_sub | ">" add_sub | ">=" add_sub)*
    def relational(self):
        node = self.add_sub()
        while True:
            token = self.current_token
            if self.current_token.type == TokenType.TK_LT:
                self.eat(TokenType.TK_LT)
                node = BinaryOp_Node(left=node, op=token, right=self.add_sub())
                continue
            if self.current_token.type == TokenType.TK_LE:
                self.eat(TokenType.TK_LE)
                node = BinaryOp_Node(left=node, op=token, right=self.add_sub())
                continue
            if self.current_token.type == TokenType.TK_GT:
                self.eat(TokenType.TK_GT)
                node = BinaryOp_Node(left=node, op=token, right=self.add_sub())
                continue
            if self.current_token.type == TokenType.TK_GE:
                self.eat(TokenType.TK_GE)
                node = BinaryOp_Node(left=node, op=token, right=self.add_sub())
                continue
            return node


    # equality = relational ("==" relational | "! =" relational)*
    def equality(self):
        node = self.relational()
        while True:
            token = self.current_token
            if self.current_token.type == TokenType.TK_EQ:
                self.eat(TokenType.TK_EQ)
                node = BinaryOp_Node(left=node, op=token, right=self.relational())
                continue
            if self.current_token.type == TokenType.TK_NE:
                self.eat(TokenType.TK_NE)
                node = BinaryOp_Node(left=node, op=token, right=self.relational())
                continue
            return node

    # expr = equality
    def expression(self):
        node = self.equality()
        return node

    def parse(self):
        """
        expr = equality
        equality = relational ("==" relational | "! =" relational)*
        relational = add_sub ("<" add_sub | "<=" add_sub | ">" add_sub | ">=" add_sub)*
        add_sub = mul_div ("+" mul_div | "-" mul_div)*
        mul_div = unary ("*" unary | "/" unary)*
        unary = ("+" | "-")? primary
        primary = num | "(" expr ")"
        """
        node = self.expression()
        if self.current_token.type != TokenType.TK_EOF:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token,
            )
        return node
