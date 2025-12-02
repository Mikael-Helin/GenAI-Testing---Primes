def fast_prime_sum(limit):
    X = 1  # Initial value
    prime_sum = 0
    is_prime = [True] * (limit + 1)  # Array to mark prime numbers

    # Pre-calculate primes for efficiency (Sieve of Eratosthenes)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    # Generate the sequence and calculate prime sum
    for _ in range(limit): 
        if is_prime[X]:
            prime_sum += X
        X = ((2147483647 * X + 137438953471) % 1400 + 1)

    return prime_sum

result = fast_prime_sum(100_000_000)
print("The sum of prime numbers in the sequence is:", result)