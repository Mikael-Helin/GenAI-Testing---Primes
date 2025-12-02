import random

# Initialize the RNG with the given seed
random.seed(1)

# Sieve of Eratosthenes to find all primes up to a given limit
def sieve_of_eratosthenes(limit):
    prime = [True for _ in range(limit + 1)]
    p = 2
    while (p * p <= limit):
        if (prime[p] == True):
            for i in range(p * p, limit + 1, p):
                prime[i] = False
        p += 1
    prime[0], prime[1] = False, False  # 0 and 1 are not primes
    prime_numbers = [p for p in range(limit + 1) if prime[p]]
    return prime_numbers

# Adjust here: Use 100000000 as the limit for generating all primes up to 100,000,000
primes_set = set(sieve_of_eratosthenes(100000000))

# Function to sum all prime numbers in the generated sequence using the comprehensive list of primes
def sum_primes_with_full_list(limit, primes_set):
    total_sum = 0
    for _ in range(limit):
        num = random.randint(1, 100000000)
        if num in primes_set:
            total_sum += num
    return total_sum

# Adjust the number of iterations as needed. For the full task, it's 100000000.
# Note: Running this with the full 100000000 iterations will be very resource-intensive and time-consuming.
print(sum_primes_with_full_list(100000000, primes_set), len(primes_set))