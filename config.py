from sympy import Heaviside, DiracDelta, exp
from symbols import *

# Process Parameters
KpFlat = 5
TpFlat = 2
TnFlat = .1
ZetaFlat = .1
ThetaPFlat = 0

# Disturbance Parameters
KdFlat = 5

# Controls Parameters
KcFlat = 2
TiFlat = float('inf')
TdFlat = 0

# Influence Functions
delta_ysp = 1
delta_d = 0

# Transfer Functions
# Gp = Kp / (Tp*s + 1) * exp(-ThetaP*s)  # FOPDT
# Gp = Kp / ((Tn**2)*(s**2) + 2*Zeta*Tn*s + 1) * exp(-ThetaP*s) # SOPDT
Gp = Kp / (1*s) * exp(-ThetaP*s)  # IPDT
Gc = Kc + Kc / (Ti * s) + Kc * Td * s  # PID
Gd = Kd
