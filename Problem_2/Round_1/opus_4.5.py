#!/usr/bin/env python3
"""
Sum all primes from random sequence X(1) to X(10^8) where:
    random.seed(1)
    X(i) = random.randint(1, 100000000)

Strategy:
1. Build sieve of Eratosthenes for primes up to 10^8 (odd numbers only to save memory)
2. Iterate through 10^8 random numbers, summing primes

Optimizations:
- Odd-only sieve: halves memory usage (50MB instead of 100MB)
- Slice assignment for sieve building (much faster than loops)
- Local variable caching to avoid repeated lookups
- Bitwise operations where possible
"""
import random

def main():
    random.seed(1)
    
    N = 100_000_000
    LIMIT = 100_000_001  # Need to check up to 10^8
    
    print("Building sieve...")
    
    # Sieve for odd numbers only
    # Index i represents number 2*i + 1
    # sieve[i] = 0 means prime, 1 means composite
    half = LIMIT >> 1
    sieve = bytearray(half)
    sieve[0] = 1  # 1 is not prime
    
    # Sieve of Eratosthenes with slice assignment (much faster)
    sqrt_limit = int(LIMIT ** 0.5) // 2 + 1
    for i in range(1, sqrt_limit):
        if not sieve[i]:
            p = (i << 1) + 1  # p = 2*i + 1
            start = (p * p) >> 1  # index of p*p
            # Mark all odd multiples of p as composite
            count = len(range(start, half, p))
            sieve[start::p] = b'\x01' * count
    
    print("Sieve complete. Summing primes...")
    
    # Sum primes from random sequence
    # Optimization: check odd first (50% of cases), handle rare x==2 separately
    total = 0
    count_2 = 0
    randint = random.randint  # Local cache for speed
    
    for _ in range(N):
        x = randint(1, 100000000)
        if x & 1:  # odd - most common case first
            if not sieve[x >> 1]:
                total += x
        elif x == 2:  # rare: probability 1/10^8
            count_2 += 1
    
    total += 2 * count_2
    
    print(f"\nSum of primes: {total}")
    return total

if __name__ == "__main__":
    main()