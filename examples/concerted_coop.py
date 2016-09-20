import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..'))

import sympy as sp

from crnpy.crn import CRN, from_react_file

__author__ = "Elisa Tonello"
__copyright__ = "Copyright (c) 2016, Elisa Tonello"
__license__ = "BSD"
__version__ = "0.0.1"

# Concerted model of cooperativity.
# Ingalls, Brian. "Mathematical Modelling in Systems Biology: An Introduction.", 2013.
# 3.7.11

filename = "data/reactions/concerted_coop"
crn = from_react_file(filename)
print(crn.derivative('2*R2X2 + 2*T2X2 + R2X + T2X + X'))
crn.inspect(True)

crn.rapid_eq('R2X2', 'R2X + X')
crn.rapid_eq('T2X2', 'T2X + X')
crn.rapid_eq('R2X', 'R2 + X')
crn.rapid_eq('T2X', 'T2 + X')
crn.rapid_eq('R2', 'T2')

print("")
print(crn.removed_species)
print("")

saturation = sp.sympify('(T2X + R2X + 2*T2X2 + 2*R2X2)/2/(T2 + R2 + T2X + R2X + T2X2 + R2X2)')
for variable, expr in crn.removed_species:
    saturation = saturation.subs(variable, expr).simplify()
print("Saturation: {}".format(saturation))

Y = sp.sympify("(K*X/KT*(1+X/KT)+X/KR*(1+X/KR))/(K*(1+X/KT)**2+(1+X/KR)**2)"). \
                   subs("K", sp.sympify("k_1/k1")). \
                   subs("KT", sp.sympify("k_2/k2")). \
                   subs("KR", sp.sympify("k_3/k3")).simplify()

print(sp.simplify(saturation.expand() - Y.expand() ) == 0)
