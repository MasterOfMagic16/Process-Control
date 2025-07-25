from sympy.integrals import laplace_transform, inverse_laplace_transform
from sympy import solve, exp
from sympy.plotting import plot
from config import *
from symbols import *

# Take Laplace Transform
LaplaceODE = laplace_transform(ODE, t, s, noconds=True)

# Replace Symbols
deltaU = laplace_transform(deltau, t, s, noconds=True)
LaplaceODE = LaplaceODE.subs({
    laplace_transform(deltay(t), t, s, noconds=True): deltaY,
    laplace_transform(deltau, t, s, noconds=True): deltaU,
    deltay(0): 0,
    diff(deltay(t), t).subs(t, 0): 0
})

# Define Transfer Function
Gp = solve(LaplaceODE, deltaY)[0] / deltaU

# Add Dead Time
Gp = Gp * exp(-ThetaP * s)

# Substitute parameters
Gp = Gp.subs({
    Kp: KpFlat,
    Tp: TpFlat,
    Tn: TnFlat,
    Zeta: ZetaFlat,
    ThetaP: ThetaPFlat,
})

# Inverse Laplace
deltaY = Gp * deltaU
deltay = inverse_laplace_transform(deltaY, s, t)

print(deltay)

# Plot Function
p1 = plot(deltay)




