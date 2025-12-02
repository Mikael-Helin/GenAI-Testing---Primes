# ------------------------------------------------------------
#  FAST PURE-PYTHON SOLVER
#  Uses EXACT SAME random algorithm as Python's "random" module
#  No imports, no shortcuts, deterministic identical sequence.
# ------------------------------------------------------------

# -------------------- MT19937 --------------------

N = 624
M = 397
A = 0x9908b0df
UPPER = 0x80000000
LOWER = 0x7fffffff
B = 0x9d2c5680
C = 0xefc60000

mt = [0]*N
idx = N+1

def seed_MT(s):
    global idx
    mt[0] = s & 0xffffffff
    for i in range(1, N):
        mt[i] = (1812433253*(mt[i-1]^(mt[i-1]>>30)) + i) & 0xffffffff
    idx = N

def twist():
    for i in range(N):
        y = (mt[i] & UPPER) | (mt[(i+1) % N] & LOWER)
        mt[i] = mt[(i+M) % N] ^ (y>>1) ^ (A if (y & 1) else 0)

def rand32():
    global idx
    if idx >= N:
        twist()
        idx = 0

    y = mt[idx]
    idx += 1

    # Tempering (identical to CPython)
    y ^= (y >> 11)
    y ^= (y << 7) & B
    y ^= (y << 15) & C
    y ^= (y >> 18)
    return y & 0xffffffff

# -------------------- EXACT CPython random.random() --------------------
# random() = ((a << 26) + b) / 2**53
# a = rand32() >> 5    # top 27 bits
# b = rand32() >> 6    # top 26 bits

def random_fixed53():
    a = rand32() >> 5
    b = rand32() >> 6
    return (a << 26) + b   # still an integer (0 .. 2**53-1)

# -------------------- EXACT CPython randint(1, 100000000) --------------------
# randint uses: floor(random()*n) + 1
# Here: floor(random()*100000000)+1
#
# Instead of floats, we do integer scaling:
# floor((fixed53 / 2**53) * n)
# → floor(fixed53 * n / 2**53)

NMAX = 100000000
SHIFT = 53
MASK53 = (1 << SHIFT)

def randint_1_100M():
    r = random_fixed53()
    return (r * NMAX >> SHIFT) + 1

# -------------------- Fast deterministic primality (32-bit) --------------------

def is_prime(n):
    if n < 2:
        return False
    if not (n & 1):
        return n == 2

    # write n-1 = d * 2^s
    d = n - 1
    s = 0
    while (d & 1) == 0:
        d >>= 1
        s += 1

    # deterministic bases for 32-bit integers
    for a in (2, 7, 61):
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(s-1):
            x = (x*x) % n
            if x == n-1:
                break
        else:
            return False
    return True

# -------------------- MAIN LOOP --------------------

seed_MT(1)

total = 0
for _ in range(100_000_000):
    v = randint_1_100M()
    if is_prime(v):
        total += v

print(total)
