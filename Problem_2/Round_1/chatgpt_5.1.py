# Fastest possible pure-Python solver
# Absolutely no imports used.

# ----- Reimplementation of MT19937 (Python's random uses this) -----

# Constants from CPython Modules/_randommodule.c
N = 624
M = 397
MATRIX_A = 0x9908b0df
UPPER_MASK = 0x80000000
LOWER_MASK = 0x7fffffff

# State array
mt = [0] * N
mti = N + 1

def seed_mt(seed):
    global mti
    mt[0] = seed & 0xffffffff
    for i in range(1, N):
        mt[i] = (1812433253 * (mt[i-1] ^ (mt[i-1] >> 30)) + i) & 0xffffffff
    mti = N

def extract_number():
    global mti
    if mti >= N:
        # twist
        for i in range(N):
            y = (mt[i] & UPPER_MASK) | (mt[(i+1) % N] & LOWER_MASK)
            mt[i] = mt[(i+M) % N] ^ (y >> 1) ^ (MATRIX_A if (y & 1) else 0)
        mti = 0

    y = mt[mti]
    mti += 1

    # tempering
    y ^= (y >> 11)
    y ^= (y << 7) & 0x9d2c5680
    y ^= (y << 15) & 0xefc60000
    y ^= (y >> 18)
    return y & 0xffffffff

# ----- reimplementation of CPython's random.random() -----

def random_double():
    # produces same double as CPython random()
    a = extract_number() >> 5
    b = extract_number() >> 6
    return (a * 67108864.0 + b) / 9007199254740992.0

# ----- reimplementation of randint(1, 100000000) -----

def randint():
    return int(random_double() * 100000000.0) + 1


# ----- sieve of primes up to 100M (but we don't sieve whole) -----

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = 3
    # no imports → rewrite sqrt loop
    limit = 1
    while limit * limit <= n:
        limit += 1
    while r <= limit:
        if n % r == 0:
            return False
        r += 2
    return True


# --- cycle detection & analytic counting ---

def solve(N=100000000):
    seed_mt(1)

    seen = {}   # value → index
    seq = []    # store generated numbers until cycle

    x = randint()
    i = 0

    while x not in seen:
        seen[x] = i
        seq.append(x)
        i += 1
        x = randint()

    mu = seen[x]        # start of cycle
    lam = len(seq) - mu # cycle length

    # count occurrences
    counts = {}
    for v in seq[:mu]:
        counts[v] = counts.get(v, 0) + 1

    cycle = seq[mu:]
    cycle_count = {}
    for v in cycle:
        cycle_count[v] = cycle_count.get(v, 0) + 1

    remaining = N - mu
    full = remaining // lam
    tail = remaining % lam

    for v, c in cycle_count.items():
        counts[v] = counts.get(v, 0) + c * full

    for v in cycle[:tail]:
        counts[v] = counts.get(v, 0) + 1

    # sum primes
    s = 0
    for v, c in counts.items():
        if is_prime(v):
            s += v * c
    return s


# Running the solver:
print(solve())
