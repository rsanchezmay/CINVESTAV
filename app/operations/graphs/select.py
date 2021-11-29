def select():
    s = input('Elige un parametreo para graficar [s1, s2, s3, s4 o s para graficar todos] ')
    if s == 's':
        n = 5
        m = 5
    elif s == 's1':
        n = 0
        m = 0
    elif s == 's2':
        n = 0
        m = 1
    elif s == 's3':
        n = 1
        m = 0
    elif s == 's4':
        n = 1
        m = 1
    return n, m
