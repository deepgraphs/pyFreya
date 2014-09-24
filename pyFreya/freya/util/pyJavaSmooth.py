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