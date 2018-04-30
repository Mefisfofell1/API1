
id = 263717343
from string import ascii_letters, digits

from itertools import product

from random import *
letters = ascii_letters+digits
import hashlib
for N in range(6,7):


    for x in product(letters,repeat=N):

        test_string = str(id)+'-'+"".join(x)
        if hashlib.md5(test_string.encode('utf8')).hexdigest()[:6] == '000000':
            print(test_string)

