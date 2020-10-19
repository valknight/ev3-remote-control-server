from random import randint, SystemRandom
import string

def generate_code(n=6, onlyInts=True):
    if onlyInts:
        join_code = ''.join(["{}".format(randint(0, 9))
                            for num in range(0, n)])
    else:
        join_code = ''.join(SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(n))
    return join_code

def generate_joincode(n=6):
    join_code = generate_code(n=n)
    print("Join code: {}".format(join_code))
    with open('joinCode', 'w') as f:
        f.write(join_code)
    return join_code