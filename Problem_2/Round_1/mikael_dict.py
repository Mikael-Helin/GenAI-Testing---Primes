import random
random.seed(1)

# Set your parameters

Xmax = 100000000# max value
N = int(1E8)    # number of iterations

# Build a Boolean array of primes

# Build a dictoinary of primes
primes = {}
primes[2] = True
for i in range(3, Xmax, 2):
    primes[i] = True
for i in range(3, Xmax, 2):
    if primes[i]:
        for j in range(i*i, Xmax, i):
            primes[j] = False
            
# Print largest prime
# print("Largest prime: ", max([k for k, v in primes.items() if v]))

# Generate the sequence and sum the primes
sum_primes = 0
for _ in range(N):
    X = random.randint(1, Xmax)
    if primes.get(X, False):
        sum_primes += X

print("Sum of primes: ", sum_primes)