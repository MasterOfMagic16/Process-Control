from sympy.solvers import solve
from sympy import diff, lambdify, ode_order
import matplotlib.pyplot as plt
import pandas as pd

from symbols import *


def Main(GUIData):
    # TODO: There is a derivative control discrepancy
    # TODO: Make deadtime work
    # TODO: Animate

    # Simulation Settings
    resolution = GUIData["StepSize"]
    timeEnd = GUIData["Duration"]

    # Pull GUI data used most often
    processType = GUIData["ProcessType"]

    # General Functions
    delta_y = Function("delta_y")

    # Define Controller Output
    delta_ysp = GUIData["SetPointStepChange"]
    delta_e = delta_ysp - delta_y(t)
    delta_c = 0
    if GUIData["ControlType"]["pControl"]:
        delta_c += Kc * delta_e
    if GUIData["ControlType"]["iControl"]:
        delta_c += Kc / Ti * integral_error
    if GUIData["ControlType"]["dControl"]:
        delta_c += Kc * Td * diff(delta_e, t)

    # Define Process Manual Control ODE, Controlled By Controller
    delta_d = GUIData["DisturbanceStepChange"]
    delta_u = delta_c
    if processType == "I":
        ODE = diff(delta_y(t), t) - Kp * delta_u - Kd * delta_d
    elif processType == "FO":
        ODE = Tp * diff(delta_y(t), t) + 1 * delta_y(t) - Kp * delta_u - Kd * delta_d
    elif processType == "SO":
        ODE = (Tn ** 2) * diff(diff(delta_y(t), t), t) + 2*Zeta*Tn*diff(delta_y(t), t) + 1*delta_y(t) - Kp * delta_u - Kd * delta_d
    else:
        print(f"Process Type: {processType} is not supported")
        raise ValueError()
    if GUIData["DeadTimeType"]:
        pass
    ODE = ODE.subs(
        GUIData["Parameters"]
    )

    # Define Initial Conditions
    integrated_error = 0
    time = 0
    timeList = [time]
    delta_yList = [0]

    # Solve for useful things
    order = ode_order(ODE, delta_y(t))
    highestOrderDeriv = solve(ODE, diff(delta_y(t), (t, order)))[0]

    # Define The Highest Order Derivative Equation
    # Define Initial Conditions
    lambdas = []
    derivList = []
    for i in range(0, order):
        lambdas.append(diff(delta_y(t), (t, i)))
        derivList.append(0)
    lambdas.append(integral_error)

    highestOrderDeriv = lambdify(lambdas, highestOrderDeriv, 'numpy')
    derivList.append(highestOrderDeriv(*derivList, integrated_error))

    while time <= timeEnd:
        time += resolution
        for i in range(len(derivList)-1):
            derivList[i] += derivList[i+1]*resolution
        error = delta_ysp - derivList[0]
        integrated_error += error*resolution
        derivList[-1] = highestOrderDeriv(*derivList[0:-1], integrated_error)
        timeList.append(time)
        delta_yList.append(derivList[0])

    df = pd.DataFrame({
        "Time (s)": timeList,
        "Output (delta_y)": delta_yList
    })
    df.to_excel("simulation_output.xlsx", index=False)
    print("Excel file saved as simulation_output.xlsx")

    plt.plot(timeList, delta_yList)
    plt.show()


