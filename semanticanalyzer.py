import sys

from parser import *

###############################################################################
#
#   Symbols
#
###############################################################################

class Symbol:
    pass


class Var_Symbol(Symbol):
    def __init__(self, var_name, var_type, offset):
        self.var_name = var_name        # variable name
        self.var_type = var_type
        self.offset = offset       # offset from RSP


class SymbolTable:
    def __init__(self):
        self._symbols = {}

    def insert(self, symbol):
        self._symbols[symbol.var_name] = symbol

    def lookup(self, name):
        # 'symbol' is either an instance of the Symbol class or None
        symbol = self._symbols.get(name)
        if symbol is not None:
            return symbol


###############################################################################
#                                                                             #
#  SEMANTIC-ANALYZER                                                                     #
#                                                                                #
###############################################################################


class SemanticAnalyzer(NodeVisitor):
    def __init__(self, tree):
        self.depth = 0
        self.tree = tree
        self.symbol_table = SymbolTable()
        self.stack_size = 0
        self.offset = 0

    def visit_UnaryOp_Node(self, node):
        pass

    def visit_Return_Node(self, node):
        self.visit(node.right)

    def visit_BinaryOp_Node(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Assign_Node(self, node):
        # make sure the left side of assign is a varible
        if node.left.token.type != TokenType.TK_IDENT:
            print(f"the left side of assign is not a variable", file=sys.stderr)
        self.visit(node.left)
        self.visit(node.right)

    def visit_Block_Node(self, node):
        for eachnode in node.statement_nodes:
            self.visit(eachnode)

    def visit_Num_Node(self, node):
        pass

    def visit_Var_Node(self, node):
        var_name = node.value
        var_symbol = self.symbol_table.lookup(var_name)
        if var_symbol is None:
            print(f"semantic error, var not declared", file=sys.stderr)
            sys.exit(1)

    def visit_VarDecl_Node(self, node):
        var_name = node.var_node.value
        var_symbol = self.symbol_table.lookup(var_name)
        if var_symbol is None:
            # We have some information we need to create a variable symbol.
            # Create the symbol and insert it into the symbol table.
            var_type = node.type_node.value
            self.offset += 8
            var_offset = -self.offset
            var_symbol = Var_Symbol(var_name, var_type, var_offset)
            self.symbol_table.insert(var_symbol)

    def semantic_analyze(self):
        # Traverse the AST to construct symbol table.
        tree = self.tree
        for node in tree:
            if node is not None:
                self.visit(node)

        return self.symbol_table, self.offset