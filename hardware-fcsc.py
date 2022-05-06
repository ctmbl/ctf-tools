def gate1(x):
    return bit_not(x) & round_left(x)

def bit_not(num,nb_bits=63):
    return num ^ ((1 << nb_bits) - 1)

def solve(x):
    return x ^ round_left(gate1(x))

def round_left(x, nb_bits=63):
    return ((x << 1) % (0b1 << nb_bits)) + (x >> nb_bits-1)

def force_it():
    for i in range(1<<63):
        if i % (1<<61) == 0:
            print(i)
        if solve(i) == 8549048879922979409:
            print(i)
            return

def is_set(x, n):
    return 1 if (x & 2 ** n != 0) else 0

def incr_gate1(x, n):
    return 1 if (is_set(x,n) and not is_set(x, n+1)) else 0

def next_x(y, seed):
    return is_set(y,seed[1]) ^ incr_gate1(seed[0], seed[1]-2)    

def solve_it(y,seed):
    while seed[1] != 63:
        seed[0] += next_x(y,seed) << seed[1]
        seed[1] += 1
    print(seed)
