from sympy.integrals import laplace_transform, inverse_laplace_transform
from sympy import solve, exp
from sympy.plotting import plot
from config import *
from symbols import *


def GetTransferFunction(ODE, output, forcing):
    # Take Laplace Transform
    LaplaceODE = laplace_transform(ODE, t, s, noconds=True)

    # Replace Symbols
    Forcing = laplace_transform(forcing, t, s, noconds=True)
    LaplaceODE = LaplaceODE.subs({
        laplace_transform(output(t), t, s, noconds=True): Output,
        laplace_transform(forcing, t, s, noconds=True): Forcing,
        output(0): 0,
        diff(output(t), t).subs(t, 0): 0
    })

    # Define Transfer Function
    G = solve(LaplaceODE, Output)[0] / Forcing

    # Add Dead Time
    G = G * exp(-ThetaP * s)

    # Substitute parameters
    G = G.subs({
        Kp: KpFlat,
        Tp: TpFlat,
        Tn: TnFlat,
        Zeta: ZetaFlat,
        ThetaP: ThetaPFlat,
        Kc: KcFlat,
        Ti: TiFlat,
        Td: TdFlat
    })

    return G, Forcing


Gp, deltaU = GetTransferFunction(ProcessODE, deltay, deltau)
deltaY = Gp * deltaU

# Inverse Laplace
deltay = inverse_laplace_transform(deltaY, s, t)

# Plot Function
p1 = plot(deltay)

# Controls
ControllerODE = Kc * deltae(t) - deltac(t)

Gc, deltaE = GetTransferFunction(ControllerODE, deltac, deltae)
deltaC = Gc * deltaE

# Inverse Laplace
deltac = inverse_laplace_transform(deltaC, s, t)
print(deltaC)
