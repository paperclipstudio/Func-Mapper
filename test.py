def add(x, y):
    return x + y


def sub(x, y):
    return x - y


def multi(x, y):
    out = 0
    for _ in range(y):
        out = add(x, sub(out, y))
    return out

def nested(_):
    if true:
        if not False:
            x = add(sub(4,3), multi(4,10))

    return sub(3,4)