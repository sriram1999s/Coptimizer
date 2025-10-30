# Bit Hacks Cheat Sheet

Compact summary of bit-level optimizations in our project.

---

## 1. Min of two integers (`validate_find_min`)
```c
res = rhs ^ ((lhs ^ rhs) & -(lhs < rhs));
```
Branchless `min(lhs, rhs)` for `int`/`char`.

## 2. Modulo of sum (`validate_compute_mod`)
```c
(x + y) - (n & -((x + y) >= n))
```
Branchless `(x+y) % n` for `(x+y) < 2n`.

## 3. Absolute value (`validate_find_abs`)
```c
mask = x >> (sizeof(int)*CHAR_BIT - 1);
abs_x = (x + mask) ^ mask;
```
Branchless `abs(x)`.

## 4. Power of 2 check (`validate_power_of_2`)
```c
x && !(x & (x - 1))
```
Detects if `x` is a power of 2.

## 5. Count set bits (`validate_count_set_bits`)
```c
BitsSetTable[x & 0xff] + BitsSetTable[(x>>8)&0xff] + ...
```
Table-lookup instead of iterative bit count.

## 6. Unique characters (`application_unique_characters`)
```c
checker & (1 << (char - 'a'))
checker |= (1 << (char - 'a'))
```
Detects duplicates using bit vector.

## 7. Sort & deduplicate positive integers (`application_sort_unique_positive`)
```c
BitVec[array[i]/32] |= 1 << (array[i]%32)
```
Bit vector tracks presence of numbers.

## 8. Sort positive integers with duplicates (`application_sort_positive`)
```c
BitVec[hash] |= 1 << lsb
BitVec[hash] &= ~(1 << lsb)
```
Bit manipulation to handle duplicates efficiently.

