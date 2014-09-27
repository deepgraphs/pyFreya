__author__ = 'root'
def isset(a):
    try:
        a
    except NameError:
        return False
    else:
        return True
def JArray2List(a):
    ret=list()
    for doc in a:
        ret.append(doc)
    return ret
def contains(small, big):
    for i in xrange(len(big)-len(small)+1):
        for j in xrange(len(small)):
            if big[i+j] != small[j]:
                break
        else:
            return i, i+len(small)
    return False