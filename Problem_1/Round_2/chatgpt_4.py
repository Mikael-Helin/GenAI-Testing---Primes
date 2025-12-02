def sieve_primes(n):
    """Use Sieve of Eratosthenes to find all primes up to n."""
    prime = [True for _ in range(n+1)]
    p = 2
    while (p * p <= n):
        if (prime[p] == True):
            for i in range(p * p, n+1, p):
                prime[i] = False
        p += 1
    primes = [p for p in range(2, n) if prime[p]]
    return primes

def optimized_sum_prime_sequence(limit, mod_val, multiplier, increment):
    """Optimized function to generate sequence and sum primes using cycle detection."""
    # Precompute primes up to mod_val
    primes = sieve_primes(mod_val)
    primes_set = set(primes)

    # Find cycle in the sequence
    seen = {}
    x = 1  # Initial value
    sequence = []
    while x not in seen:
        seen[x] = len(sequence)
        sequence.append(x)
        x = ((multiplier * x + increment) % mod_val + 1)
        if x in seen:  # Cycle detected
            cycle_start = seen[x]
            cycle = sequence[cycle_start:]
            break

    # Calculate the sum of prime numbers within the cycle
    cycle_prime_sum = sum(x for x in cycle if x in primes_set)

    # Calculate how many complete cycles fit into limit and the sum for the partial cycle at the end
    cycle_length = len(cycle)
    total_cycles = limit // cycle_length
    partial_cycle_length = limit % cycle_length

    # Sum for complete cycles and the partial cycle
    total_sum = cycle_prime_sum * total_cycles
    total_sum += sum(sequence[i] for i in range(partial_cycle_length) if sequence[i] in primes_set)

    return total_sum

# Constants for the sequence
LIMIT = 100000000
MOD_VAL = 1400
MULTIPLIER = 2147483647
INCREMENT = 137438953471

# Using optimized approach to calculate the sum of primes
optimized_sum = optimized_sum_prime_sequence(LIMIT, MOD_VAL, MULTIPLIER, INCREMENT)
print(optimized_sum)