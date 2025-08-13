from sympy.solvers import solve
from sympy import diff, lambdify, ode_order
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

from symbols import *

derivListSize = 3

class Simulation:
    def __init__(self):
        pass

    def Reset(self, GUIData=None):
        print("Called")
        self.time = 0
        self.integrated_error = 0
        self.realDerivList = []
        self.seenDerivList = []
        self.realDerivListCache = []
        for i in range(0, derivListSize):
            self.realDerivList.append(0)
            self.seenDerivList.append(0)
        self.realDerivListCache.append(self.realDerivList.copy())

        self.timeList = []
        self.delta_yList = []
        self.delta_cList = []

        if GUIData:
            self.UpdateParams(GUIData)

        self.SetUpGraph()


    def UpdateParams(self, GUIData):
        print("UpdateCalled")
        # General Variables
        delta_y = Function("delta_y")

        processType = GUIData["ProcessType"]
        self.resolution = GUIData["StepSize"]
        # self.timeEnd = GUIData["Duration"]
        self.deadTime = GUIData["Parameters"]["ThetaP"] if GUIData["DeadTimeType"] else 0
        self.batchno = int(.05 / self.resolution)

        # Define Controller
        self.delta_ysp = GUIData["SetPointStepChange"]
        delta_e = self.delta_ysp - delta_y(t)
        delta_c = 0 * t  # TODO: Kinda Weird
        if GUIData["ControlType"]["pControl"]:
            delta_c += Kc * delta_e
        if GUIData["ControlType"]["iControl"]:
            delta_c += Kc / Ti * integral_error
        if GUIData["ControlType"]["dControl"]:
            delta_c += Kc * Td * diff(delta_e, t)
        self.delta_c = delta_c.subs(
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
            ODE = (Tn ** 2) * diff(diff(delta_y(t), t), t) + 2 * Zeta * Tn * diff(delta_y(t), t) + 1 * delta_y(t) - Kp * delta_u - Kd * delta_d
        else:
            print(f"Process Type: {processType} is not supported")
            raise ValueError()
        ODE = ODE.subs(
            GUIData["Parameters"]
        )

        lambdas = []
        self.order = ode_order(ODE, delta_y(t))
        for i in range(0, self.order):
            lambdas.append(diff(delta_y(t), (t, i)))
        lambdas.append(integral_error)

        highestOrderDeriv = solve(ODE, diff(delta_y(t), (t, self.order)))[0]

        self.highestOrderDerivFunc = lambdify(lambdas, highestOrderDeriv, 'numpy')
        self.controllerFunc = lambdify([delta_y(t), diff(delta_y(t)), integral_error], delta_c, 'numpy')

    def GeneratePoint(self):
        # New Time
        self.time += self.resolution

        # Update Real Process. Seen Deriv List is from last time step
        for i in range(self.order):
            self.realDerivList[i] += self.realDerivList[i + 1] * self.resolution
        error = self.delta_ysp - self.seenDerivList[0]
        self.integrated_error += error * self.resolution


        self.realDerivList[self.order] = self.highestOrderDerivFunc(*self.realDerivList[0:self.order], self.integrated_error)
        self.realDerivListCache.append(self.realDerivList.copy())

        # Update Seen Process
        if self.time >= self.deadTime:
            self.seenDerivList = self.realDerivListCache.pop(0)

        # Update Curves
        self.timeList.append(self.time)
        self.delta_yList.append(self.seenDerivList[0])
        self.delta_cList.append(self.controllerFunc(*self.seenDerivList[0:2], self.integrated_error))


    def SetUpGraph(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(self.time - 5, self.time + 1)
        self.line, = self.ax.plot([], [], 'g-')

        self.ani = animation.FuncAnimation(self.fig, self.UpdateGraph, init_func=self.InitGraph, blit=False,
                                      interval=1000 * self.resolution * self.batchno,cache_frame_data=False)

        plt.show()

    def InitGraph(self):
        self.line.set_data([],[])
        return self.line,

    def UpdateGraph(self, frame):
        # Generate Batches of Points
        for i in range(self.batchno):
            self.GeneratePoint()
        self.line.set_data(self.timeList, self.delta_yList)
        self.ax.relim()
        self.ax.autoscale_view(scalex=False, scaley=True)

        self.ax.set_xlim(0, self.time + 1)

        return self.line,


    def ExportCurve(self):
        df = pd.DataFrame({
            "Time (s)": self.timeList,
            "Output (delta_y)": self.delta_yList,
            "Controller": self.delta_cList
        })
        df.to_excel("simulation_output.xlsx", index=False)
        print("Excel file saved as simulation_output.xlsx")

    # TODO: There is a derivative control discrepancy
    # TODO: Animate
    # TODO: order deteriorates if 0 on parameter
    # TODO: Error handling for incorrect entries (Ti = 0)
