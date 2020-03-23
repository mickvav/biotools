#!/usr/bin/env python3
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
#
#  E'  = phi - c1 * n1 - c2 * n2
#
#  n1' = (E>0 ? a1 * n1 : -b1 * n1) - d1 * np
#  n2' = (E>0 ? a2 * n2 : -b2 * n2) - d2 * np
#
#  np' = -g1*np + r1*n1 + r2*n2
#

phi = 10.0
c1 = 0.1
c2 = 0.1
a1 = 0.016
a2 = 0.008 ## RM slows down growth
b1 = 0.0001 ## death is slower, when no energy around
b2 = 0.00012 ## RM speeds up death, when no energy is present
d1 = 0.001
d2 = 0.0001 ## RM lowers phage impact
g1 = 0.001
r1 = 0.001
r2 = 0.0001

def codyn(y, t):
    E, n1, n2, np = y
    dydt = [
        phi - c1 * n1 - c2 * n2,
        ((a1*n1 if E>0 else -b1*n1) - d1 * np) if n1 > 0 else 0,
        ((a2*n2 if E>0 else -b2*n2) - d2 * np) if n2 > 0 else 0,
        -g1*np + r1*(n1 if n1>0 else 0) + r2*(n2 if n2>0 else 0)
    ]
    return dydt

nmax = 100000000
t = np.linspace(0, 100000, nmax)
y0 = [ 1.0, 10.0, 10.0, 2.0 ]
sol = odeint(codyn, y0, t)
print(sol)

plt.plot(t[range(0,nmax,100)], sol[range(0,nmax,100), 0], 'r', label='E')
plt.plot(t[range(0,nmax,100)], sol[range(0,nmax,100), 1], 'b', label='b1 (without RM)')
plt.plot(t[range(0,nmax,100)], sol[range(0,nmax,100), 2], 'g', label='b2 (with RM)')
plt.plot(t[range(0,nmax,100)], sol[range(0,nmax,100), 3], 'y', label='p')
plt.legend(loc='best')
plt.xlabel('t')
plt.grid()
plt.show()
a=input()
