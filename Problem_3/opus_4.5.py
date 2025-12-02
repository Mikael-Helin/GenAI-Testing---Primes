#!/usr/bin/env python3
"""
Find the largest prime where all digits are different.

Key insight: Sum of 0-9 = 45, divisible by 3.
So 10-digit pandigitals are all divisible by 3.
We need 9 digits, dropping one that makes sum not divisible by 3.
Drop d where (45-d) % 3 != 0: d in {1, 2, 4, 5, 7, 8}

To maximize, prioritize dropping smallest digits that keep largest digits.
Order: drop 1, then 2, then 4, then 5, then 7, then 8
"""

def is_prime(n):
    """Miller-Rabin primality test - deterministic for n < 3,317,044,064,679,887,385,961,981"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    if n < 9:
        return True
    if n % 3 == 0:
        return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witnesses sufficient for numbers up to 3,317,044,064,679,887,385,961,981
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    
    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_perms_descending(digits):
    """Generate all permutations of digits in descending numerical order."""
    digits = sorted(digits, reverse=True)
    n = len(digits)
    
    # Start with largest permutation
    current = digits[:]
    
    while True:
        # Skip if leading zero
        if current[0] != 0:
            yield int(''.join(map(str, current)))
        
        # Find next permutation in descending order
        # (This is finding previous permutation in ascending order)
        i = n - 2
        while i >= 0 and current[i] <= current[i + 1]:
            i -= 1
        
        if i < 0:
            break
        
        j = n - 1
        while current[j] >= current[i]:
            j -= 1
        
        current[i], current[j] = current[j], current[i]
        current[i + 1:] = reversed(current[i + 1:])


def main():
    all_digits = set(range(10))
    
    # Order to drop digits: prioritize keeping largest digits
    # Drop 1 first (max potential 987654320), then 2, 4, 5, 7, 8
    drop_order = [1, 2, 4, 5, 7, 8]
    
    best_prime = 0
    
    for drop in drop_order:
        digits = list(all_digits - {drop})
        max_possible = int(''.join(map(str, sorted(digits, reverse=True))))
        
        # If max possible is less than best found, skip this digit set
        if max_possible <= best_prime:
            print(f"Drop {drop}: max={max_possible} <= best={best_prime}, skipping")
            continue
        
        print(f"Drop {drop}: checking permutations (max={max_possible})...")
        
        count = 0
        for num in generate_perms_descending(digits):
            if num <= best_prime:
                break  # All remaining perms will be smaller
            
            count += 1
            if is_prime(num):
                print(f"  Found prime: {num}")
                best_prime = num
                break
        
        print(f"  Checked {count} permutations")
    
    print(f"\nLargest prime with distinct digits: {best_prime}")
    return best_prime


if __name__ == "__main__":
    main()