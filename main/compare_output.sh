#!/bin/sh

#./home/c0dey0da/Documents/Capstone/main/exec.sh $1
gcc $1 -o inp
gcc output.c -o out

./inp > inp_res
./out > out_res

# diff inp_res out_res
# echo $0



