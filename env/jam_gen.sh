#!/bin/sh

./Coptimizer $1
rm our orig
gcc output.c -o our
gcc $1 -o orig
