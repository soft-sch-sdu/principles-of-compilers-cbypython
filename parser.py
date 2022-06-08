from lexer import *

###############################################################################
#
#   AST_Node type:
#   UnaryOp_Node         : +, -
#   BinaryOp_Node        : +, -, *, /, <, <=, >, >=, ==, !=
#   Num_Node             : num
#
###############################################################################


class AST_Node:
    def __init__(self):
        self.next = None


class UnaryOp_Node(AST_Node):
    def __init__(self, op, right):
        self.next = None
        self.token = self.op = op
        self.right = right

class Return_Node(AST_Node):
    def __init__(self, tok, right):
        self.next = None
        self.token = tok
        self.right = right

class Block_Node(AST_Node):
    def __init__(self, ltok, rtok, statement_nodes):
        self.next = None
        self.ltoken = ltok
        self.rtoken = rtok
        self.statement_nodes = statement_nodes

class BinaryOp_Node(AST_Node):
    def __init__(self, left, op, right):
        self.next = None
        self.left = left
        self.token = self.op = op
        self.right = right


class Assign_Node(AST_Node):
    def __init__(self, left, op, right):
        self.next = None
        self.left = left
        self.token = self.op = op
        self.right = right


class Num_Node(AST_Node):
    def __init__(self, token):
        self.next = None
        self.token = token
        self.value = token.value


class Var_Node(AST_Node):
    """The Var node is constructed out of ID token."""
    def __init__(self, token):
        self.next = None
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

    # primary = "(" expr ")" | ident | num
    def primary(self):
        token = self.current_token

        # "(" expr ")"
        if token.type == TokenType.TK_LPAREN:
            self.eat(TokenType.TK_LPAREN)
            node = self.expression()
            self.eat(TokenType.TK_RPAREN)
            return node
        # ident
        elif token.type == TokenType.TK_IDENT:
            self.eat(TokenType.TK_IDENT)
            return Var_Node(token)
        # num
        elif token.type == TokenType.TK_INTEGER_CONST:
            self.eat(TokenType.TK_INTEGER_CONST)
            return Num_Node(token)

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

    # assign = equality ("=" assign)?
    def assign(self):
        node = self.equality()
        token = self.current_token
        if token.type == TokenType.TK_ASSIGN:
            self.eat(TokenType.TK_ASSIGN)
            node = Assign_Node(left=node, op=token, right = self.assign())
        return node

    # expression = assign
    def expression(self):
        node = self.assign()
        return node

    # expression-statement = expression? ";"
    def expression_statement(self):
        token = self.current_token
        node = None
        if token.type == TokenType.TK_SEMICOLON:
            self.eat(TokenType.TK_SEMICOLON)
        else:
            node = self.expression()
            self.eat(TokenType.TK_SEMICOLON)
        return node


    # statement = expression-statement
    #             | "return" expression-statement
    #             | "{" compound_statement "}"
    def statement(self):
        token = self.current_token
        if token.type == TokenType.TK_RETURN:
            self.eat(TokenType.TK_RETURN)
            node = Return_Node(tok=token, right = self.expression_statement())
            return node
        if token.type == TokenType.TK_LBRACE:
            ltok = self.current_token  # "{"
            self.eat(TokenType.TK_LBRACE)
            statement_nodes = self.compound_statement()
            rtok = self.current_token  # "}"
            self.eat(TokenType.TK_RBRACE)
            node  = Block_Node(ltok, rtok, statement_nodes)
            return node
        return self.expression_statement()

    # compound_statement = statement*
    def compound_statement(self):
        statement_nodes = []
        while self.current_token.type != TokenType.TK_RBRACE:
            node = self.statement()
            if node is not None: # abandon "  ;", i.e., null statement
                statement_nodes.append(node)
        return statement_nodes


    # program = statement*
    def parse(self):
        """
        program = statement*
        statement = expression-statement
                    | "return" expression-statement
                    | "{" compound_statement "}"
        compound_statement = statement*
        expression-statement = expression? ";"
        expression = assign
        assign = equality ("=" assign)?
        equality = relational ("==" relational | "! =" relational)*
        relational = add_sub ("<" add_sub | "<=" add_sub | ">" add_sub | ">=" add_sub)*
        add_sub = mul_div ("+" mul_div | "-" mul_div)*
        mul_div = unary ("*" unary | "/" unary)*
        unary = ("+" | "-")? primary
        primary = "(" expr ")" | ident | num
        """

        statement_nodes = []
        while self.current_token.type != TokenType.TK_EOF:
            node = self.statement()
            statement_nodes.append(node)
        if self.current_token.type != TokenType.TK_EOF:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token,
            )
        return statement_nodes
