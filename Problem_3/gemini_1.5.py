import itertools

def is_prime(num):
    """Checks if a number is prime using a basic implementation."""
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def find_largest_unique_digit_prime():
    """Finds the largest prime number with unique digits, smaller than 9876543210."""
    for num_digits in range(7, 10):
        for digits in itertools.permutations(range(1, num_digits + 1), num_digits):
            candidate = int(''.join(map(str, digits)))
            if candidate % 2 != 0 and candidate % 5 != 0 and is_prime(candidate):  # Pruning
                return candidate

    return None

result = find_largest_unique_digit_prime()
if result:
    print("The largest prime with unique digits is:", result)
else:
    print("No prime found within the given range.")
    