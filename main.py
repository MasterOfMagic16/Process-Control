from sympy.integrals import laplace_transform, inverse_laplace_transform
from sympy.plotting import plot
from config import *
from symbols import *


# Function for flattening into numeric graph
def Substitute(function):
    return function.subs({
        Kp: KpFlat,
        Tp: TpFlat,
        Tn: TnFlat,
        Zeta: ZetaFlat,
        ThetaP: ThetaPFlat,
        Kd: KdFlat,
        Kc: KcFlat,
        Ti: TiFlat,
        Td: TdFlat
    })


# Laplace Transforms
delta_Ysp = laplace_transform(delta_ysp, t, s)[0]
delta_D = laplace_transform(delta_d, t, s)[0]

# Standard Control Loop
delta_Y = Gp*Gc / (1 + Gp*Gc) * delta_Ysp + Gd / (1 + Gp*Gc) * delta_D
delta_Y = Substitute(delta_Y)

# Inverse Laplace
delta_y = inverse_laplace_transform(delta_Y, s, t)

# Plot Function
p1 = plot(delta_y)

print(delta_y)

result = delta_y.subs({
    t: 1000
})

print(result)

# Offset is correct
# Setpoint Eqn integrating is correct
