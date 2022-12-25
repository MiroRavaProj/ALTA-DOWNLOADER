def dot_trick(handle):
    if handle == "":
        return
    f = lambda s: s[11:] and [s[0] + w + x for x in f(s[1:]) for w in ('.', '')] or [s]
    mail_list = f(handle)
    file =  open("scripts/emails.txt", "w")
    file.write("\n".join(map(lambda x: str(x), mail_list)))
    return

if __name__ == '__main__':
    dot_trick("Robertohjgdvh@gmail.com")
