import itertools

def is_prime(n):
    """Efficiently checks if a number is prime."""
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    
    i = 5
    # We only need to check up to sqrt(n)
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def find_largest_distinct_prime():
    # The set of digits that yields the largest magnitude 9-digit numbers
    # while having a sum not divisible by 3.
    # Digits: 0, 2, 3, 4, 5, 6, 7, 8, 9 (We excluded 1)
    digits = "987654320"
    
    print("Checking permutations of:", digits)
    
    # Generate permutations in lexicographic order (descending because input is descending)
    for p in itertools.permutations(digits):
        # Last digit optimization:
        # A prime > 5 cannot end in 0, 2, 4, 6, 8 (evens) or 5 (divisible by 5).
        last_digit = int(p[-1])
        if last_digit % 2 == 0 or last_digit == 5:
            continue
            
        # Convert tuple to integer
        num = int("".join(p))
        
        # Check primality
        if is_prime(num):
            return num

if __name__ == "__main__":
    result = find_largest_distinct_prime()
    print(f"The largest prime with unique digits is: {result}")