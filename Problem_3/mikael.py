import itertools
import numpy as np

skip_10 = False

biggest_digit_string = "9876543210"
biggest_digit_number = int(biggest_digit_string)

def find_lower_primes():
    num_max = int(np.sqrt(biggest_digit_number))
    primes = np.ones(num_max, dtype=bool)
    primes[0] = False # Remove number 1
    num = 2
    while num <= num_max:
        if primes[num - 1]:
            primes[num*num - 1:num_max:num] = False
        num += 1
    return [i+1 for i, is_prime in enumerate(primes) if is_prime]

largest_prime = 2
list_of_primes = find_lower_primes()[1:] # Remove 2

def test_is_prime(number):
    """WARNING: test invalid for primes smaller than sqrt(biggest_digit_number)"""
    global list_of_primes
    for p in list_of_primes:
        if number%p == 0:
            return False
    return True

# Testing with 10 digits
if not skip_10:
    permutations = itertools.permutations(biggest_digit_string)

# Remove even numbers and divisible by 5 and those staring with 0
def reduce_permutations(perms):
    return [perm for perm in perms if perm[-1] in ["1", "3", "7", "9"] and perm[0] != "0"]

if not skip_10:
    permutations = reduce_permutations(permutations)

# Find highest primes in permutations
highest_prime = 2
def find_highest_prime(perms):
    global highest_prime
    for perm in perms:
        number = int("".join(perm))
        if number > highest_prime and test_is_prime(number):
            highest_prime = number
    return highest_prime

if not skip_10:
    print(find_highest_prime(permutations)) # prints 2, did not find 10 digit prime

# Testing with 9 digits
permutations = itertools.permutations(biggest_digit_string, 9)
print(find_highest_prime(permutations))
