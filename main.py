from sympy.integrals import laplace_transform, inverse_laplace_transform
from sympy.plotting import plot
from sympy.solvers import solve
from sympy import exp, Heaviside, diff, Function, lambdify, Integral
from symbols import *
import matplotlib.pyplot as plt

def Main(GUIData):
    resolution = .00001
    timeEnd = 1

    processType = GUIData["ProcessType"]
    deadTimeType = GUIData["DeadTimeType"]
    pControl = GUIData["ControlType"]["pControl"]
    iControl = GUIData["ControlType"]["iControl"]
    dControl = GUIData["ControlType"]["dControl"]
    flatParams = GUIData["FlatParams"]

    delta_y = Function("delta_y")
    # Define Controller Output to ODE
    delta_ysp = GUIData["SetPointStepChange"]
    delta_e = delta_ysp - delta_y(t)
    delta_c = 0*t  # A little weird but okay
    if pControl:
        delta_c += Kc * delta_e
    if iControl:
        delta_c += Kc / Ti * Integral(delta_e, (t, 0, t))
    if dControl:
        delta_c += Kc * Td * diff(delta_e, t)

    # Define ODE Manual Control, Controlled By Controller
    delta_d = GUIData["DisturbanceStepChange"]
    delta_u = delta_c
    ODE = 0
    if processType == "I":
        ODE = diff(delta_y(t), t) - Kp * delta_u - Kd * delta_d
    elif processType == "FO":
        ODE = Tp * diff(delta_y(t), t) + 1 * delta_y(t) - Kp * delta_u - Kd * delta_d
    elif processType == "SO":
        ODE = (Tn ** 2) * diff(diff(delta_y(t), t), t) + 2*Zeta*Tn*diff(delta_y(t), t) + 1*delta_y(t) - Kp * delta_u - Kd * delta_d
    else:
        print(f"Process Type: {processType} is not supported")
        raise ValueError()
    if deadTimeType:
        pass
        # Ignore for now
    ODE = ODE.subs(
        GUIData["FlatParams"]
    )

    print(ODE)

    # Define Initial Conditions
    time = 0
    timeList = [time]
    delta_yList = [delta_y]

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



    # Iterate (ignore possible manual intervention for now)
    # while time <= timeEnd:
    #   time += resolution


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