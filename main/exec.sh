#!/bin/sh
clang-tidy $1 -fix -checks="readability-braces-around-statements,readability-isolate-declaration" -- COMPILE_OPTIONS
python3 code/detector.py $1 ;
indent -kr temp.c -o output.c;
rm code/parser.out code/parsetab.py temp.c;
rm -r code/__pycache__;
