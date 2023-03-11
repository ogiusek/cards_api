def tryremove(lst, value):
    try:
        lst.remove(value)
    except ValueError:
        pass