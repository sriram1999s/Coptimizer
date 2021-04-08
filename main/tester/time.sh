#!/bin/sh

gcc -Wall -pg $1 -o unoptimized
gcc -Wall -pg $2 -o optimized

./unoptimized > unoptimized_output 

gprof -b unoptimized gmon.out | head -n -6 > unoptimized_profile
rm gmon.out

./optimized > optimized_output 
gprof -b optimized gmon.out | head -n -6 > optimized_profile

