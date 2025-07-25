from sympy import Heaviside, DiracDelta, diff
from symbols import *
# Settings
KpFlat = 5
TpFlat = 2
TnFlat = 1
ZetaFlat = .5
ThetaPFlat = 5

# deltau = DiracDelta(t)
deltau = 10 * Heaviside(t)

# ODE = Tp * diff(deltay(t), t) + deltay(t) - Kp * deltau  # First Order
# ODE = Tn**2 * diff(diff(deltay(t), t), t) + 2*Zeta*Tn*diff(deltay(t), t) + 1*deltay(t) - Kp * deltau  # Second Order
ODE = diff(deltay(t), t) - Kp * deltau     # Integrating

# Could have a list of ODEs and run a for loop, then multiply transfer functions for higher order process
