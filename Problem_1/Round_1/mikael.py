# Put all primes into a dictionary

def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    for m in range(3, n):
        if n%m == 0:
            return False
    return True

primes = {}
for p in range(1400):
    if is_prime(p):
        primes[p] = True

# Initialize variables

X = 1
primes_sum = X if primes.get(X, False) else 0

# Computing the sum of primes in a for loop

for _ in range(100000000):
    X = ((2147483647*X + 137438953471) % 1400 + 1)
    if primes.get(X, False):
        primes_sum += X

# Print the result

print(primes_sum)