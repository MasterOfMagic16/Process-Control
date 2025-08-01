from sympy.integrals import laplace_transform, inverse_laplace_transform
from sympy.plotting import plot
from sympy.solvers import solve
from sympy import exp, diff, lambdify, ode_order
from symbols import *
import matplotlib.pyplot as plt
import pandas as pd

def Main(GUIData):
    if not GUIData["Laplace"]:
        # TODO: Fix derivative control discrepancy
        # TODO
        # Make it look nicer
        # Make deadtime work
        # Animate
        # Add a legend

        # Simulation Settings TODO: Add to GUI
        resolution = .001
        timeEnd = 10

        # Pull GUI data used most often
        processType = GUIData["ProcessType"]

        # General Functions
        delta_y = Function("delta_y")

        # Define Controller Output
        delta_ysp = GUIData["SetPointStepChange"]
        delta_e = delta_ysp - delta_y(t)
        delta_c = 0 * t  # TODO: A little weird but okay
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
            # TODO: Allow For Deadtime
        ODE = ODE.subs(
            GUIData["FlatParams"]
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
        plt.plot(timeList, delta_yList)
        plt.show()

        df = pd.DataFrame({
            "Time (s)": timeList,
            "Output (delta_y)": delta_yList
        })
        df.to_excel("simulation_output.xlsx", index=False)
        print("Excel file saved as simulation_output.xlsx")

    else:
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
            Gp = Kp / (Tp * s + 1)
        elif processType == "SO":
            Gp = Kp / ((Tn ** 2) * (s ** 2) + (2 * Zeta * Tn * s) + 1)
        else:
            print(f"Process Type: {processType} is not supported")
            raise ValueError()
        if deadTimeType:
            Gp = Gp * exp(-ThetaP * s)

        # Set Gc
        Gc = 0
        if pControl:
            Gc += Kc
        if iControl:
            Gc += Kc / (Ti * s)
        if dControl:
            Gc += Kc * Td * s
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
        delta_Y = Gp * Ga * Gc / (1 + Gp * Ga * Gc * Gs) * delta_Ysp + Gd / (1 + Gp * Ga * Gc * Gs) * delta_D

        # Flatten
        delta_Y = delta_Y.subs(GUIData["FlatParams"])

        # Inverse Laplace
        delta_y = inverse_laplace_transform(delta_Y, s, t)

        # Plot
        p1 = plot(delta_y)
