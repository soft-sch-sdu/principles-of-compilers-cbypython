###############################################################################
#                                                                             #
#  CODE-GENERATOR                                                                     #
#                                                                                #
###############################################################################

from parser import *

class Codegenerator(NodeVisitor):
    def __init__(self, tree, symbol_table, offset):
        self.depth = 0
        self.tree = tree
        self.symbol_table = symbol_table
        self.offset = offset


    # Round up `n` to the nearest multiple of `align`. For instance,
    # align_to(5, 8) returns 8 and align_to(11, 8) returns 16.
    def align_to(self, n, align):
      return int((n + align - 1) / align) * align


    def visit_UnaryOp_Node(self, node):
        self.visit(node.right)
        if node.op.type == TokenType.TK_MINUS:
            print(f"  neg %rax")

    def visit_BinaryOp_Node(self, node):
        self.visit(node.right)
        print(f"  push %rax")
        self.visit(node.left)
        print(f"  pop %rdi")
        if node.op.type == TokenType.TK_PLUS:
            print(f"  add %rdi, %rax")
        elif node.op.type == TokenType.TK_MINUS:
            print(f"  sub %rdi, %rax")
        elif node.op.type == TokenType.TK_MUL:
            print(f"  imul %rdi, %rax")
        elif node.op.type == TokenType.TK_DIV:
            print(f"  cqo")
            print(f"  idiv %rdi")
        elif node.op.type == TokenType.TK_EQ:
            print(f"  cmp %rdi, %rax")
            print(f"  sete %al")
            print(f"  movzb %al, %rax")
        elif node.op.type == TokenType.TK_NE:
            print(f"  cmp %rdi, %rax")
            print(f"  setne %al")
            print(f"  movzb %al, %rax")
        elif node.op.type == TokenType.TK_LT:
            print(f"  cmp %rdi, %rax")
            print(f"  setl %al")
            print(f"  movzb %al, %rax")
        elif node.op.type == TokenType.TK_GT:
            print(f"  cmp %rdi, %rax")
            print(f"  setg %al")
            print(f"  movzb %al, %rax")
        elif node.op.type == TokenType.TK_LE:
            print(f"  cmp %rdi, %rax")
            print(f"  setle %al")
            print(f"  movzb %al, %rax")
        elif node.op.type == TokenType.TK_GE:
            print(f"  cmp %rdi, %rax")
            print(f"  setge %al")
            print(f"  movzb %al, %rax")


    def visit_Assign_Node(self, node):
            if node.left.token.type == TokenType.TK_IDENT:
                # var is left-value
                symbol = self.symbol_table.lookup(node.left.token.value)
                offset = symbol.offset
                print(f"  lea {offset}(%rbp), %rax")
                # left-value
                print(f"  push %rax")

                self.visit(node.right)
                print(f"  pop %rdi")
                print(f"  mov %rax, (%rdi)")
            else:
                error("not an lvalue");

    def visit_Num_Node(self, node):
        print(f"  mov ${node.value}, %rax")

    def visit_Var_Node(self, node):
        # var is right-value
        symbol = self.symbol_table.lookup(node.value)
        offset = symbol.offset
        print(f"  lea {offset}(%rbp), %rax")
        # right-value
        print(f"  mov (%rax), %rax");


    def code_generate(self):
        print(f"  .globl main")
        print(f"main:")
        # Prologue
        print(f"  push %rbp")
        print(f"  mov %rsp, %rbp")
        stack_size = self.align_to(self.offset, 16)
        print(f"  sub ${stack_size}, %rsp")

        # Traverse the AST to emit assembly.
        tree = self.tree
        for node in tree:
            self.visit(node)

        # Epilogue
        print(f"  mov %rbp, %rsp")
        print(f"  pop %rbp")
        print(f"  ret")
        assert (self.depth == 0)
