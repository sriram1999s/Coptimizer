#!/bin/sh
clang-tidy $1 -fix -checks="readability-braces-around-statements,readability-isolate-declaration" -- COMPILE_OPTIONS
python3 ../src/controller.py $1 ;
indent -linux temp.c -o output.c;
rm ../src/parser.out ../src/parsetab.py temp.c;
rm -r ../src/__pycache__;
