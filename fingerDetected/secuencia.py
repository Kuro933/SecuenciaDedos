import random

def secuencia():
    i=0
    secuencia = []
    
    while i < 10:
        rnd = random.randrange(0,5)
        if i != 0:
            if secuencia[i-1] != rnd:
                secuencia.append(rnd)
                i += 1
        else:
            secuencia.append(rnd)
            i += 1

    i = 0
    return secuencia


