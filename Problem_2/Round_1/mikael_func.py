import random
random.seed(1)

# Set your parameters

Xmax = 100000000# max value
N = int(1E8)    # number of iterations

# Build a Boolean array of primes

primes = [True] * Xmax
primes[0] = False
p=2
while p*p <= Xmax:
    if primes[p-1]:
        for i in range(p*p - 1, Xmax, p):
            primes[i] = False
    p += 1

# Print largest prime
for i in range(Xmax, 0, -1):
    if primes[i-1]:
        print("Largest prime: ", i)
        break

# Generate the sequence and sum and pass in the primes
def sum_primes(primes, N, Xmax):
    sum_primes = 0
    for _ in range(N):
        X = random.randint(1, Xmax)
        if primes[X-1]:
            sum_primes += X
    return sum_primes

print("Sum of primes: ", sum_primes(primes, N, Xmax))