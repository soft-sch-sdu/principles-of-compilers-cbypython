import argparse
import sys


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

    print(f"  .globl main")
    print(f"main:")
    print(f"  mov ${args.input}, %rax")
    print(f"  ret")

if __name__ == '__main__':
    main()
