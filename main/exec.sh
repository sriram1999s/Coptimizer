#!/bin/sh

python3 code/detector.py $1 ;
gindent -linux temp.c -o output.c;
rm code/parser.out code/parsetab.py temp.c;
rm -r code/__pycache__;