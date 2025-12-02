def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    """Generate a list of prime numbers up to n."""
    primes = []
    for num in range(2, n+1):
        if is_prime(num):
            primes.append(num)
    return primes

def sum_prime_sequence(limit, mod_val, multiplier, increment):
    """Generate sequence and sum primes."""
    # Precompute primes up to mod_val
    primes_set = set(generate_primes(mod_val))
    x = 1  # Initial value
    prime_sum = 0
    
    for _ in range(limit):
        if x in primes_set:
            prime_sum += x
        x = ((multiplier * x + increment) % mod_val + 1)
    
    return prime_sum

# Constants for the sequence
LIMIT = 100000000
MOD_VAL = 1400
MULTIPLIER = 2147483647
INCREMENT = 137438953471

# Sum prime numbers in the sequence
sum_primes = sum_prime_sequence(LIMIT, MOD_VAL, MULTIPLIER, INCREMENT)
print(sum_primes)