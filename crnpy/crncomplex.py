#!/usr/bin/env python

"""Complex class."""

from collections import Counter
import sympy as sp

__author__ = "Elisa Tonello"
__copyright__ = "Copyright (c) 2016, Elisa Tonello"
__license__ = "BSD"
__version__ = "0.0.1"


class Complex(Counter):
    """A complex is represented with a counter.
    A complex can be created from a dictionary or an iterable.

    :Example:

    >>> c1 = Complex({'S': 2, 'E': 1})
    >>> c1
    E + 2S
    >>> c2 = Complex('SSE')
    >>> c3 = Complex(S = 2, E = 1)
    >>> c1 == c2 == c3
    True

    From the collections.Counter documentation:

    "class collections.Counter([iterable-or-mapping])
     A Counter is a dict subclass for counting hashable objects.
     It is an unordered collection where elements are stored as dictionary keys
     and their counts are stored as dictionary values.
     Counts are allowed to be any integer value including zero or negative counts.
     The Counter class is similar to bags or multisets in other languages."
    """
    def __str__(self):
        return " + ".join([(str(v) if v != 1 else "") + str(k) for k, v in sorted(self.items())])

    def  __repr__(self):
        return self.__str__()

    def  __lt__(self, other):
        return all(k in other for k in self) and \
               all(self[k] <= other[k] for k in self) and \
               (any(self[k] < other[k] for k in self) or \
                any(k not in self for k in other))

    def  __le__(self, other):
        return all(k in other for k in self) and \
               all(self[k] <= other[k] for k in self)

    def  __gt__(self, other):
        return all(k in self for k in other) and \
               all(self[k] >= other[k] for k in other) and \
               (any(self[k] > other[k] for k in other) or \
                any(k not in other for k in self))

    def  __ge__(self, other):
        return all(k in self for k in other) and \
               all(self[k] >= other[k] for k in other)

    def times(self, n):
        """Return the complex obtained by multiplying
        all stoichiometric coefficients by n.

        :Example:

        >>> Complex(a = 1, b = 3).times(2)
        2a + 6b

        :rtype: Complex.
        """
        if not isinstance(n, int):
            raise ValueError("Can only multiply stoichiometric coefficients by integer.")
        if n == 0:
            return Complex({})
        mult = Complex(self)
        for k in mult.keys(): mult[k] = mult[k] * n
        return mult

    def ma(self):
        """Return the mass action monomial associated to the complex.

        :Example:

        >>> c1 = Complex({'S': 2, 'E': 1})
        >>> c1.ma()
        E*S**2

        :rtype: sympy expression.
        """
        if self == {}: return 1
        return sp.Mul(*(sp.Symbol(r)**self[r] for r in self))

    def to_vector(self, species):
        """Return a vector (sympy matrix of dimentions (number of species) times 1)
        containing the stoichiometric cofficients of species in complex.

        :Example:

        >>> c1 = Complex({'S': 2, 'E': 1})
        >>> c1.to_vector(['E', 'C', 'S', 'P'])
        Matrix([
        [1],
        [0],
        [2],
        [0]])

        :rtype: sympy Matrix.
        """
        return sp.Matrix([self[s] if s in self else 0 for s in species])

    def symp(self):
        """Return a sympy expression representing the complex.

        :Example:

        >>> Complex({'S': 2, 'E': 1}).symp()
        E + 2*S

        :rtype: sympy expression.
        """
        return sp.Add(*(self[s]*sp.Symbol(s) for s in self))
