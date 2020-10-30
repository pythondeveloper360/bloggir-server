def encrypt(string):
    value = string[::-1]
    l = []
    for i in range(len(value)):
        l.append(ord(value[i]))
    return l

def decrypt(list):
    s = ''
    for i in range(len(list)):
        s+= chr(list[i])
    return s[::-1]

def uniqueslug(slug,slugs):
    nums = [chr(i) for i in range(47,56)]
