# Find the largest prime with all digits different (each digit appears at most once).
# Strategy:
# - Try lengths from 10 down to 1.
# - For each length L, iterate permutations of digits '9'..'0' taken L at a time in lexicographic order
#   based on descending digit list so we find larger numbers first.
# - Skip permutations where first digit is '0' (leading zero).
# - Test primality with a deterministic Miller-Rabin suitable for 64-bit integers.
# - Stop when the first (largest) prime is found.
#
# This will print the prime and the code used.

from itertools import permutations
import math

# Deterministic Miller-Rabin for n < 2^64 using known bases
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    small_primes = [2,3,5,7,11,13,17,19,23,29]
    for p in small_primes:
        if n % p == 0:
            return n == p
    # write n-1 as d*2^s with d odd
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    # bases to test - sufficient for n < 2^64
    bases = [2,325,9375,28178,450775,9780504,1795265022]
    def check(a, s, d, n):
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            return True
        for _ in range(s-1):
            x = (x * x) % n
            if x == n-1:
                return True
        return False
    for a in bases:
        if a % n == 0:
            continue
        if not check(a, s, d, n):
            return False
    return True

digits = [str(d) for d in range(9, -1, -1)]  # '9','8',...,'0'

found = None
found_len = None
count_checked = 0

for L in range(10, 0, -1):
    # iterate permutations of length L
    for tup in permutations(digits, L):
        if tup[0] == '0':  # leading zero -> skip
            continue
        # construct number
        n = int(''.join(tup))
        count_checked += 1
        if is_prime(n):
            found = n
            found_len = L
            break
    if found is not None:
        break

print(found, found_len, count_checked)

