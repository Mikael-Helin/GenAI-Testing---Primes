import sys

def solve():
    # Target iteration count
    TARGET_N = 100_000_000
    MOD = 1400
    
    # --- 1. Sieve of Eratosthenes ---
    # We only need primes up to the max possible value of the generator (1400)
    # is_prime[i] will be True if i is prime
    is_prime = [True] * (MOD + 2)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int((MOD + 2)**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, MOD + 2, i):
                is_prime[j] = False

    # --- 2. Cycle Detection ---
    # Constants for the generator reduced by MOD to keep math small
    # X(n+1) = (A * X(n) + B) % MOD + 1
    # We pre-calculate A % MOD and B % MOD
    A = 2147483647 % MOD
    B = 137438953471 % MOD
    
    # Store the sequence to identify the cycle
    sequence = [1]        # Stores values X(0), X(1)...
    seen_at = {1: 0}      # Map value -> index where it first appeared
    
    curr = 1
    cycle_start_index = -1
    cycle_length = -1
    
    # Iterate until we find a repeat. 
    # Max iterations needed is 1401 (Pigeonhole principle)
    while True:
        # Generator formula
        curr = (A * curr + B) % MOD + 1
        
        if curr in seen_at:
            cycle_start_index = seen_at[curr]
            cycle_length = len(sequence) - cycle_start_index
            break
        
        seen_at[curr] = len(sequence)
        sequence.append(curr)

    # --- 3. Calculate Sum ---
    # We need the sum of primes for X(1) ... X(TARGET_N).
    # Note: sequence list contains X(0) at index 0.
    
    # Separate the sequence into the "Head" (non-repeating) and "Cycle" (repeating)
    # We slice from 1 because we must exclude X(0)
    
    # Identify the part of the list before the cycle starts, excluding X(0)
    head_part = sequence[1 : cycle_start_index]
    
    # Identify the repeating cycle part
    cycle_part = sequence[cycle_start_index:]
    
    # Sum primes in the Head
    total_sum = sum(x for x in head_part if is_prime[x])
    
    # Calculate how many items are left to sum after the head
    remaining_items = TARGET_N - len(head_part)
    
    # Calculate contribution of the Cycles
    if remaining_items > 0:
        # Sum of primes in one single cycle
        cycle_prime_sum = sum(x for x in cycle_part if is_prime[x])
        
        # How many full loops of the cycle fit in the remaining items?
        full_cycles = remaining_items // cycle_length
        total_sum += full_cycles * cycle_prime_sum
        
        # How many items are left over after the full cycles?
        remainder = remaining_items % cycle_length
        
        # Sum the primes in the remainder part of the cycle
        # We take the first 'remainder' elements of the cycle_part
        total_sum += sum(x for x in cycle_part[:remainder] if is_prime[x])

    print(f"Total Sum: {total_sum}")

if __name__ == "__main__":
    solve()