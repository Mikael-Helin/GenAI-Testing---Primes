def fast_prime_sum_cycle(limit):
    X = 1
    prime_sum = 0
    seen = set()  # To keep track of visited sequence values

    # Pre-compute some primes for initial checks
    primes = set()
    for i in range(2, int(limit**0.5) + 1):
        if i not in primes:
            primes.add(i)
            for j in range(i * i, limit + 1, i):
                primes.add(j)  

    # Cycle Detection 
    while X not in seen:
        seen.add(X)
        if X in primes:
            prime_sum += X
        X = (2147483647 * X + 137438953471) % 1400 

    # Find cycle start and end
    cycle_start = X  # Value where cycle begins
    cycle_length = 0
    cycle_prime_sum = 0
    while True:
        X = ((2147483647 * X + 137438953471) % 1400 + 1)
        cycle_length += 1
        if X in primes:
            cycle_prime_sum += X
        if X == cycle_start:
            break

    # Extrapolate
    full_cycles = limit // cycle_length
    remaining = limit % cycle_length

    total_sum = full_cycles * cycle_prime_sum

    # Add up primes in the remaining partial cycle
    for _ in range(remaining):
        if X in primes:
            total_sum += X
        X = (2147483647 * X + 137438953471) % 1400 

    return total_sum

result = fast_prime_sum_cycle(100_000_000)
print("The sum of prime numbers in the sequence is:", result)