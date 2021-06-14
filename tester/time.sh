#!/bin/sh

gcc -Wall -pg $1 -o unoptimized
gcc -Wall -pg $2 -o optimized

./unoptimized < inp > unoptimized_output 

gprof unoptimized gmon.out | head -n -6 > unoptimized_profile
rm gmon.out

./optimized < inp > optimized_output 
gprof optimized gmon.out | head -n -6 > optimized_profile

rm unoptimized
rm optimized gmon.out