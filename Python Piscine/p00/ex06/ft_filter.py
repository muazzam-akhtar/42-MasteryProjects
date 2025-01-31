def ft_filter(_str, _int):
    _splits = _str.split()
    res = []
    for i in _splits:
        if (len(i) > int(_int)):
            res.append(i)
    return res
