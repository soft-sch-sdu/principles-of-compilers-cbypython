###############################################################################
#                                                                             #
#  CODE-GENERATOR                                                                     #
#                                                                                #
###############################################################################

from parser import *

class Codegenerator(NodeVisitor):
    def __init__(self, tree):
        self.depth = 0
        self.tree = tree

    def codegenerate(self):
        print(f"  .globl main")
        print(f"main:")
        #Traverse the AST to emit assembly.
        tree = self.tree
        self.visit(tree)
        print(f"  ret")
        assert(self.depth == 0)

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

    def visit_Num_Node(self, node):
        print(f"  mov ${node.value}, %rax")
