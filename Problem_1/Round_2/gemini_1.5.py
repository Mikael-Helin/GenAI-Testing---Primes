def fast_prime_sum_optimized(limit):
    X = 1
    prime_sum = 0

    # Pre-compute primes (replace list with set)
    primes = set()
    for i in range(2, int(limit**0.5) + 1):
        if i not in primes:
            primes.add(i)
            for j in range(i * i, limit + 1, i):
                primes.add(j)  

    # Generate the sequence and calculate prime sum
    for _ in range(limit): 
        if X in primes:
            prime_sum += X
        X = ((2147483647 * X + 137438953471) % 1400 + 1)

    return prime_sum

result = fast_prime_sum_optimized(100_000_000)
print("The sum of prime numbers in the sequence is:", result)