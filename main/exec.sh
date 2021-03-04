#!/bin/sh
clang-tidy $1 -fix -checks="readability-braces-around-statements" -- COMPILE_OPTIONS > /dev/null
python3 code/detector.py $1 ;
indent -linux temp.c -o output.c;
rm code/parser.out code/parsetab.py temp.c;
rm -r code/__pycache__;
