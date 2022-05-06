def gate1(x):
    return bit_not(x) & round_left(x)

def bit_not(num,nb_bits=63):
    return num ^ ((1 << nb_bits) - 1)

def solve(x):
    return x ^ round_left(gate1(x))

def round_left(x, nb_bits=63):
    return ((x << 1) % (0b1 << nb_bits)) + (x >> nb_bits-1)

def solve_it():
    for i in range(1<<63):
        if i % (1<<61) == 0:
            print(i)
        if solve(i) == 8549048879922979409:
            print(i)
            return

