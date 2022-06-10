#!/bin/bash
cat <<EOF | gcc -xc -c -o tmp2.o -
#include <stdio.h>
int ret3() { return 3; }

int ret5() { return 5; }

int add(int x, int y) { return x+y; }

int sub(int x, int y) { return x-y; }

int add6(int a, int b, int c, int d, int e, int f) {
  return a+b+c+d+e+f;
}

int myprint() {printf("Hello, software school.sdu.cn!!!!!!\n");}
EOF

assert() {
  expected="$1"
  input="$2"

  python3 cbypython.py "$input" > tmp.s
  gcc -o tmp tmp.s tmp2.o
  ./tmp
  actual="$?"

  if [ "$actual" = "$expected" ]; then
    echo "$input => $actual"
  else
    echo "$input => $expected expected, but got $actual"
    exit 1
  fi
}

assert 0 "0;"
assert 40 "42 -2;"
assert 41 " 12 + 34 - 5 ;"
assert 6 "12 -2 *3;"
assert 6 "-12 +20 + (-2);"
assert 6 "-12 +20 - (+2);"
assert 10 "-12 +(+20) - (-2);"
assert 5 "25-(20);"
assert 5 "+(+5);"
assert 10 "- (- (+10));"
assert 41 ' 12 + 34 - 5 ;'
assert 47 '5+6*7;'
assert 15 '6 !=6; 5*(9-6);'
assert 4 '(3+5)/2;'
assert 10 '- 10+20;'
assert 10 '- (-10);'
assert 10 '- -10;'
assert 10 '- (- (+10));'
assert 10 '- - +10;'

assert 0 '0==1;'
assert 1 '42==42;'
assert 1 '0!=1;'
assert 0 '42!=42;'

assert 1 '0<1;'
assert 0 '1<1;'
assert 0 '2<1;'
assert 1 '0<=1;'
assert 1 '2<1; 1<=1;'
assert 0 '2<=1;'

assert 1 '1>0;'
assert 0 '1>1;'
assert 0 '1>2;'
assert 1 '1>=0;'
assert 1 '1>=1;'
assert 0 '1>=2;'

assert 9 '7; 8; 9;'
assert 9 '{int a; a =5; int b; b =9;}'
assert 6 '{int a; a =5; int b ; b= a +1;}'
assert 4 '{int _a; _a=5; int b; b = _a - 1;}'

assert 8 '{return 7+1;}'
assert 13 '{return 7+2*3;}'
assert 6 '{int a; a=3; return a+3; 9;}'

assert 9 '{7; 8; 9;}'
assert 9 '{int _a; _a =5; int b; b =9;}'

assert 9 '{7; ; 9;}'
assert 14 '{int _a; _a=5; ;; ; int b; b = _a + 9;;;;}'

assert 3 '{ return ret3(); }'
assert 5 '{ return ret5(); }'
assert 9 '{ ret3()+5; 9; }'

assert 21 '{ return add6(1,1+1,3,4,5,6); }'
assert 27 '{ return add6(2,3,4,5,6,3+4); }'
assert 33 '{ return add6(3,4,5,6,7,8); }'
assert 66 '{ return add6(1,2,add6(3,4,5,6,7,8),9,10,11); }'
assert 136 '{ return add6(1,2,add6(3,add6(4,5,6,7,8,9),10,11,12,13),14,15,16); }'

assert 6 '{myprint(); return 6; }'
echo OK
