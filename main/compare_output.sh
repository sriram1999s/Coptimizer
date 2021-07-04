#!/bin/sh

sh ./exec.sh $1 > /dev/null
gcc $1 -o inp
gcc output.c -o out

echo "\n\nprovide input for both ..\n"
./inp > inp_res
./out > out_res

echo "\ninp_res:"
cat inp_res

echo "\nout_res:"
cat out_res

echo "\ndiff : \n"

echo `diff inp_res out_res`

rm inp out inp_res out_res output.c
