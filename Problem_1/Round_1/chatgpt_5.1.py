#!/usr/bin/env python3
# No external libraries. Fast cycle-counting solution.

def sum_primes_in_sequence(N=10**8):
    MOD = 1400
    # Precompute constants reduced modulo 1400:
    A = 2147483647 % MOD  # = 1247
    B = 137438953471 % MOD  # = 71

    # Generate sequence X(1), X(2), ... until cycle detected
    seen = [-1] * (MOD + 1)   # seen[value] = index in sequence list when first seen (0-based for X(1))
    seq = []                  # list of values in order (X(1), X(2), ...)
    
    # X0 = 1, so compute X1:
    x = (A * 1 + B) % MOD + 1
    idx = 0
    while seen[x] == -1:
        seen[x] = idx
        seq.append(x)
        idx += 1
        # next x
        x = (A * x + B) % MOD + 1

    mu = seen[x]              # start index of cycle in seq (0-based)
    lam = len(seq) - mu       # cycle length

    # If N smaller than length before we even find cycle, handle directly:
    if N <= len(seq):
        # count primes among first N elements
        limit = 1400
        is_prime = sieve(limit)
        s = 0
        for v in seq[:N]:
            if is_prime[v]:
                s += v
        return s

    # Count occurrences for each value among first N terms.
    counts = [0] * (MOD + 1)   # index 0 unused; values are 1..1400

    # Prefix (preperiod): seq[0:mu]
    for v in seq[:mu]:
        counts[v] += 1

    # Cycle part: seq[mu:]
    cycle = seq[mu:]
    cycle_count = [0] * (MOD + 1)
    for v in cycle:
        cycle_count[v] += 1

    remaining = N - mu
    full_cycles = remaining // lam
    tail = remaining % lam

    # Add full cycles
    if full_cycles:
        mul = full_cycles
        # add cycle_count * mul to counts
        for val in range(1, MOD + 1):
            if cycle_count[val]:
                counts[val] += cycle_count[val] * mul

    # Add tail (first 'tail' elements of cycle)
    for v in cycle[:tail]:
        counts[v] += 1

    # Sieve primes up to 1400
    is_prime = sieve(1400)

    # Sum primes weighted by counts
    total = 0
    for v in range(2, 1401):
        if is_prime[v]:
            c = counts[v]
            if c:
                total += v * c

    return total

def sieve(n):
    """Return boolean list is_prime[0..n] (True for primes)."""
    is_prime = [False, False] + [True] * (n - 1)
    import math
    lim = int(math.isqrt(n))
    for p in range(2, lim + 1):
        if is_prime[p]:
            step = p
            start = p * p
            for q in range(start, n + 1, step):
                is_prime[q] = False
    return is_prime

if __name__ == "__main__":
    N = 10**8
    result = sum_primes_in_sequence(N)
    print(result)
