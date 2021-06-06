#!/bin/sh

./Coptimizer $1
gcc output.c -o our
gcc $1 -o orig
