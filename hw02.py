HW_SOURCE_FILE = 'hw02.py'

def square(x):
    return x * x

def triple(x):
    return 3 * x

def identity(x):
    return x

def increment(x):
    return x + 1

def product(n, term):
    """Return the product of the first n terms in a sequence.

    n    -- a positive integer
    term -- a function that takes one argument

    >>> product(3, increment) # 1 * 2 * 3
    6
    >>> product(5, increment) # 1 * 2 * 3 * 4 * 5
    120
    >>> product(3, increment)   # 1^2 * 2^2 * 3^2
    6
    >>> product(5, increment)   # 1^2 * 2^2 * 3^2 * 4^2 * 5^2
    120
    """
    total, k = 1, 1
    while k <= n:
        total, k = total * term(k), k + 1
    return total

def product(n, term):
    """Return the product of the first n terms in a sequence.

        n    -- a positive integer
        term -- a function that takes one argument

        >>> product(3, identity) # 1 * 2 * 3
        6
        >>> product(5, identity) # 1 * 2 * 3 * 4 * 5
        120
        >>> product(3, identity)   # 1^2 * 2^2 * 3^2
        6
        >>> product(5, identity)   # 1^2 * 2^2 * 3^2 * 4^2 * 5^2
        120
        """
    if n==1:
        return term(1)
    else:
        return n*product(n-1, term)

def square(x):
   return x * x

def triple(x):
   return 3 * x

def identity(x):
   return x

def increment(x):
   return x + 1