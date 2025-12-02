from sympy import nextprime

# Function to generate permutations of digits and check for the largest prime
def find_largest_unique_digit_prime():
    # Try digits lengths from 9 down to 1 (since we're looking for the largest prime)
    for length in range(9, 0, -1):
        # Generate the largest number with 'length' unique digits in descending order
        max_num = int(''.join(map(str, range(9, 9-length, -1))))
        # Use nextprime with a negative step to find the next prime smaller than max_num
        prime_candidate = nextprime(max_num, -1)
        # Check if prime_candidate has unique digits and its length matches our current search length
        if len(set(str(prime_candidate))) == length:
            return prime_candidate

# Execute the function to find the largest prime with all unique digits
largest_unique_digit_prime = find_largest_unique_digit_prime()
print(largest_unique_digit_prime)