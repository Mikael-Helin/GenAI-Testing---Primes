# Set your parameters

X0 = 1          # start value
Xmax = 1400     # max value
N = 1E8         # number of iterations

# Functions

def generator(x):
    return ((2147483647*x + 137438953471) % Xmax + 1)

# Build a Boolean array of primes

primes = [True] * Xmax
primes[0] = False
p=2
while p*p <= Xmax:
    if primes[p-1]:
        for i in range(p*p - 1, Xmax, p):
            primes[i] = False
    p += 1

# Build the cycle of numbers

sequece = {}
n = 0
sequece[n] = X0
X = generator(X0)
while X != X0:
    n += 1
    sequece[n] = X
    X = generator(X)

sequece_length = len(sequece)
cycles, remaining_steps = int(N/sequece_length), N%sequece_length

# Create dictionary of position of primes in the cycle

sum_primes, position_primes = 0, {}
for i, x in sequece.items():
    if primes[x-1]:
        sum_primes, position_primes[i] = sum_primes + x, x

# Calculate the sum of primes

sum_cycled_primes = sum_primes * cycles
sum_remainder_primes = 0
for k in position_primes.keys():
    if k > remaining_steps:
        break
    sum_remainder_primes += position_primes[k]

sum_primes = sum_cycled_primes + sum_remainder_primes

print(sum_primes)
