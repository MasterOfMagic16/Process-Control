from sympy.integrals import laplace_transform, inverse_laplace_transform
from sympy.plotting import plot
from sympy.solvers import solve
from sympy import exp, Heaviside, diff, Function, lambdify, Integral, ode_order, simplify
from symbols import *
import matplotlib.pyplot as plt

def Main(GUIData):
    if not GUIData["Laplace"]:
        # TODO: Determine whether things need subscripts or not (t)
        # Simulation Settings TODO: Add to GUI
        resolution = .0001
        timeEnd = 10

        # Pull GUI data used most often
        processType = GUIData["ProcessType"]

        # General Functions
        delta_y = Function("delta_y")
        integral_error = Symbol("integrated_error")

        # Define Controller Output TODO: Verify Controller
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
        print(highestOrderDeriv)
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

        # TODO: Export CSV of Graph
        plt.plot(timeList, delta_yList)
        plt.show()
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
        print(delta_Y)

        # Inverse Laplace
        delta_y = inverse_laplace_transform(delta_Y, s, t)
        print(delta_y)

        # Plot
        p1 = plot(delta_y, delta_d * Heaviside(t), delta_ysp * Heaviside(t))

    '''
    # Try Laplace to check above
    delta_Y = Symbol("delta_Y")
    LODE = laplace_transform(ODE, t, s, noconds=True)
    print(LODE)
    LODE = LODE.subs({
        laplace_transform(delta_y(t), t, s, noconds=True): delta_Y,
        delta_y(0): 0,
    })
    if processType == "SO":
        LODE = LODE.subs({
            diff(delta_y(t), t).subs(t, 0): 0
        })
    print(LODE)
    delta_Y = solve(LODE, delta_Y)[0]
    print(delta_Y)
    delta_y = inverse_laplace_transform(delta_Y, s, t, noconds=True)

    print(delta_y)

    plt.plot(timeList, valueList)
    '''



'''
def GenerateEulerCurve(ODE):
    # Initial Conditions
    time = 0
    value = 0

    # Resolution / Limits
    h = .00001
    endTime = 10

    # Data Storage
    timeList = [time]
    valueList = [value]

    dydt = solve(ODE, diff(delta_y(t), t))[0]
    dydt = dydt.subs({
        Kp: 1,
        Tp: 10,
        delta_d(t): 2,
    })
    dydt = lambdify(delta_y(t), dydt, modules='numpy')

    # Evaluate
    while time < endTime - h:
        slope = dydt(value)
        time += h
        value += slope * h
        timeList.append(time)
        valueList.append(value)

    plt.plot(timeList, valueList)
    plt.show()
    print(valueList[-1], timeList[-1])


GenerateEulerCurve(Tp*diff(delta_y(t), t) + delta_y(t) - Kp*delta_d(t))
'''