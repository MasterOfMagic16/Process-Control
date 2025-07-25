from sympy import Heaviside, DiracDelta, diff
from symbols import *
# Settings
KpFlat = 5
TpFlat = 2
TnFlat = 1
ZetaFlat = .5
ThetaPFlat = 0

# deltau = DiracDelta(t)
deltau = 10 * Heaviside(t)

# ProcessODE = Tp * diff(deltay(t), t) + deltay(t) - Kp * deltau  # First Order
ProcessODE = Tn**2 * diff(diff(deltay(t), t), t) + 2*Zeta*Tn*diff(deltay(t), t) + 1*deltay(t) - Kp * deltau  # Second Order
# ProcessODE = diff(deltay(t), t) - Kp * deltau     # Integrating

# Could have a list of ODEs and run a for loop, then multiply transfer functions for higher order process

# Controls
setpoint = 30
KcFlat = 40
TiFlat = False
TdFlat = False