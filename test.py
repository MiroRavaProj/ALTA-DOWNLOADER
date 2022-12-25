def dot_trick(handle):
    f = lambda s:s[11:] and [s[0]+w+x for x in f(s[1:]) for w in('.','')] or [s]
    return f(handle)

if __name__ == '__main__':
    print(dot_trick("Robertohjgdvh@gmail.com"))