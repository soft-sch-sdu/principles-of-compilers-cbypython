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


    def visit_BinOp_Node(self, node):
        if node.op.type == TokenType.TK_PLUS:
            self.visit(node.right)
            print(f"  push %rax")
            self.visit(node.left)
            print(f"  pop %rdi")
            print(f"  add %rdi, %rax")
        elif node.op.type == TokenType.TK_MINUS:
            self.visit(node.right)
            print(f"  push %rax")
            self.visit(node.left)
            print(f"  pop %rdi")
            print(f"  sub %rdi, %rax")
        elif node.op.type == TokenType.TK_MUL:
            self.visit(node.right)
            print(f"  push %rax")
            self.visit(node.left)
            print(f"  pop %rdi")
            print(f"  imul %rdi, %rax")
        elif node.op.type == TokenType.TK_DIV:
            self.visit(node.right)
            print(f"  push %rax")
            self.visit(node.left)
            print(f"  pop %rdi")
            print(f"  cqo")
            print(f"  idiv %rdi")

    def visit_Num_Node(self, node):
        print(f"  mov ${node.value}, %rax")
