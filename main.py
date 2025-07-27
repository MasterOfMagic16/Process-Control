from sympy.integrals import laplace_transform, inverse_laplace_transform
from sympy.plotting import plot
from sympy import exp, Heaviside
from symbols import *


def Main(GUIData):
    processType = GUIData["ProcessType"]
    deadTimeType = GUIData["DeadTimeType"]
    pControl = GUIData["ControlType"]["pControl"]
    iControl = GUIData["ControlType"]["iControl"]
    dControl = GUIData["ControlType"]["dControl"]
    flatParams = GUIData["FlatParams"]

    # Set Gp
    Gp = 0
    if processType == "I":
        Gp = Kp / (1 * s)
    elif processType == "FO":
        Gp = Kp / (Tp*s + 1)
    elif processType == "SO":
        Gp = Kp / ((Tn**2)*(s**2) + (2*Zeta*Tn*s) + 1)
    else:
        print(f"Process Type: {processType} is not supported")
        raise ValueError()
    if deadTimeType:
        Gp = Gp*exp(-ThetaP*s)

    # Set Gc
    Gc = 0
    if pControl:
        Gc += Kc
    if iControl:
        Gc += Kc/(Ti*s)
    if dControl:
        Gc += Kc*Td*s
    # if not pControl and not iControl and not dControl:
    #   Gc = 1

    # Set Gd
    # Assume same order effect on process, I think
    Gd = Gp / Kp * Kd

    # Assume Ga = Gs = 1
    Ga = 1
    Gs = 1

    # Set Dist change and  SP change
    delta_d = GUIData["DisturbanceStepChange"]
    delta_ysp = GUIData["SetPointStepChange"]

    # Laplace Transform Input Functions
    delta_Ysp = laplace_transform(delta_ysp, t, s)[0]
    delta_D = laplace_transform(delta_d, t, s)[0]

    # Set Equation (Standard Control Loop)
    delta_Y = Gp*Ga*Gc/(1 + Gp*Ga*Gc*Gs)*delta_Ysp + Gd/(1 + Gp*Ga*Gc*Gs)*delta_D

    # Flatten
    delta_Y = delta_Y.subs(GUIData["FlatParams"])
    print(delta_Y)

    # Inverse Laplace
    delta_y = inverse_laplace_transform(delta_Y, s, t)
    print(delta_y)

    # Plot
    p1 = plot(delta_y, delta_d*Heaviside(t), delta_ysp*Heaviside(t))
