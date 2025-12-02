import random
import sys

def solve():
    # Configuration
    # We need to process 100 million numbers
    ITERATIONS = 100_000_000
    # The generator produces numbers between 1 and 100,000,000
    MAX_VAL = 100_000_000

    print("1. Generating Prime Sieve up to 100,000,000...", file=sys.stderr)
    
    # --- 1. Optimized Sieve of Eratosthenes ---
    # We use a bytearray for speed and memory efficiency.
    # 1 represents Prime, 0 represents Not Prime.
    # Initial state: Assume all are prime (1)
    is_prime = bytearray([1]) * (MAX_VAL + 1)
    
    # 0 and 1 are not prime
    is_prime[0] = 0
    is_prime[1] = 0
    
    # We only need to sieve up to sqrt(MAX_VAL)
    limit = int(MAX_VAL**0.5) + 1
    
    for i in range(2, limit):
        if is_prime[i]:
            # Python Optimization: Slice assignment is significantly faster than a for-loop.
            # We set all multiples of i starting from i*i to 0.
            # We create a bytes object of zeros of the exact length needed.
            start = i * i
            # Calculate how many multiples fit
            length = (MAX_VAL - start) // i + 1
            is_prime[start::i] = bytes(length)

    print("2. Processing 10^8 random numbers...", file=sys.stderr)

    # --- 2. Random Generation & Summation ---
    
    # IMPORTANT: We must replicate the generator exactly as specified.
    random.seed(1)
    
    # Optimization: Cache the function lookup to a local variable.
    # This saves millions of dictionary lookups inside the loop.
    rand_func = random.randint
    
    total_sum = 0
    
    # Loop 100 million times
    for _ in range(ITERATIONS):
        # Generate number
        val = rand_func(1, MAX_VAL)
        
        # O(1) Lookup: Check if it is prime using our bytearray
        if is_prime[val]:
            total_sum += val

    print(f"Total Sum: {total_sum}")

if __name__ == "__main__":
    solve()