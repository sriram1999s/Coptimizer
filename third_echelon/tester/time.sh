#!/bin/sh

gcc -Wall -pg "C:/Users/KR/PycharmProjects/Capstone/if_switch/testing/t2" -o unoptimized
gcc -Wall -pg "C:\Users\KR\PycharmProjects\Capstone\third_echelon\code\temp.c" -o optimized

./unoptimized < inp > unoptimized_output 

gprof unoptimized gmon.out | head -n -6 > unoptimized_profile
rm gmon.out

./optimized < inp > optimized_output 
gprof optimized gmon.out | head -n -6 > optimized_profile

rm unoptimized
rm optimized gmon.out
