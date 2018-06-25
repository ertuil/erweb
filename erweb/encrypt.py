'''
utils.py
~~~~~~~~~~~

This is the encript
'''

import base64

def en_xor_str(value,key,enc = 'utf-8'):
    b1 = value.encode(enc)
    b2 = key.encode(enc)
    _b2_len = len(b2)
    num = 0
    result = []
    for ii in b1:
        if num >= _b2_len:
            num = 0
        result.append(ii ^ b2[num])
        num += 1
    _str = ""
    for v in result:
        tmp = str(hex(v))[2:]
        if len(tmp) == 1:
            tmp = "0"+tmp
        _str += tmp
    return _str


def de_xor_str(value,key,enc = 'utf-8'):
    b1 = []
    ii = 0
    while ii < len(value):
        _char = value[ii:ii+2]
        b1.append(int(_char,16))
        ii += 2
    b2 = key.encode(enc)
    _b2_len = len(b2)
    num = 0
    result = []
    for ii in b1:
        if num >= _b2_len:
            num = 0
        result.append(ii ^ b2[num])
        num += 1
    return bytes(result).decode()
