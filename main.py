from sympy.solvers import solve
from sympy import diff, lambdify, ode_order
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

from symbols import *




def Main(GUIData):
    global time
    global integrated_error
    global seenDerivList

    # TODO: There is a derivative control discrepancy
    # TODO: Animate
    # TODO: order deteriorates if 0 on parameter
    # TODO: Error handling for incorrect entries (Ti = 0)

    # General Variables
    delta_y = Function("delta_y")
    processType = GUIData["ProcessType"]
    resolution = GUIData["StepSize"]
    timeEnd = GUIData["Duration"]
    deadTime = GUIData["Parameters"]["ThetaP"] if GUIData["DeadTimeType"] else 0
    batchno = int(.05 / resolution)

    # Define Controller
    delta_ysp = GUIData["SetPointStepChange"]
    delta_e = delta_ysp - delta_y(t)
    delta_c = 0 * t  # TODO: Kinda Weird
    if GUIData["ControlType"]["pControl"]:
        delta_c += Kc * delta_e
    if GUIData["ControlType"]["iControl"]:
        delta_c += Kc / Ti * integral_error
    if GUIData["ControlType"]["dControl"]:
        delta_c += Kc * Td * diff(delta_e, t)
    delta_c = delta_c.subs(
        GUIData["Parameters"]
    )

    # Define Process
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
    ODE = ODE.subs(
        GUIData["Parameters"]
    )

    # Define Initial Conditions
    time = 0
    integrated_error = 0

    # Set Lambdas / Establish Derivative Arrays At Initial Conditions
    lambdas = []
    realDerivList = []
    seenDerivList = []
    realDerivListCache = []

    order = ode_order(ODE, delta_y(t))
    for i in range(0, order):
        lambdas.append(diff(delta_y(t), (t, i)))
        realDerivList.append(0)
        seenDerivList.append(0)
    lambdas.append(integral_error)

    # Lambdify Equations
    highestOrderDeriv = solve(ODE, diff(delta_y(t), (t, order)))[0]

    highestOrderDeriv = lambdify(lambdas, highestOrderDeriv, 'numpy')
    controller = lambdify([delta_y(t), diff(delta_y(t)), integral_error], delta_c, 'numpy')

    # Finalize Derivative Lists
    realDerivList.append(highestOrderDeriv(*realDerivList, integrated_error))
    realDerivListCache.append(realDerivList.copy())
    if time >= deadTime:
        seenDerivList = realDerivListCache.pop(0)
    else:
        seenDerivList.append(0)

    # Finalize Initial Conditions
    timeList = [time]
    delta_yList = [seenDerivList[0]]
    delta_cList = [controller(*seenDerivList[0:2], integrated_error)]

    fig, ax = plt.subplots()
    ax.set_xlim(0, timeEnd)

    line, = ax.plot([], [], 'g-')

    def Init():
        line.set_data([],[])
        return line,

    def Update(frame):
        # Generate Batches of Points
        for i in range(batchno):
            GeneratePoint()
        line.set_data(timeList, delta_yList)
        ax.relim()
        ax.autoscale_view(scalex=False, scaley=True)

        window_width = 5
        ax.set_xlim(time-5, time)

        return line,

    def GeneratePoint():
        global time
        global integrated_error
        global seenDerivList

        # New Time
        time += resolution

        # Update Real Process. Seen Deriv List is from last time step
        for i in range(order):
            realDerivList[i] += realDerivList[i + 1] * resolution
        error = delta_ysp - seenDerivList[0]
        integrated_error += error * resolution
        realDerivList[-1] = highestOrderDeriv(*realDerivList[0:-1], integrated_error)
        realDerivListCache.append(realDerivList.copy())

        # Update Seen Process
        if time >= deadTime:
            seenDerivList = realDerivListCache.pop(0)

        # Update Curves
        timeList.append(time)
        delta_yList.append(seenDerivList[0])
        delta_cList.append(controller(*seenDerivList[0:2], integrated_error))

    ani = animation.FuncAnimation(fig, Update, init_func=Init, blit=False, interval=1000*resolution*batchno, cache_frame_data=False)
    plt.show()

    # Export Curve Data
    df = pd.DataFrame({
        "Time (s)": timeList,
        "Output (delta_y)": delta_yList,
        "Controller": delta_cList
    })
    df.to_excel("simulation_output.xlsx", index=False)
    print("Excel file saved as simulation_output.xlsx")

    # Plot Curve Data
