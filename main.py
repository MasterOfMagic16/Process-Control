from sympy.solvers import solve
from sympy import diff, lambdify, ode_order
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np

from symbols import *

#TODO: Controller not affecting right, doesnt actually do anything

# Configs
resolution = .05
chunkSize = 1
speedRatio = 1
windowSize = 5
derivListSize = 3


class Simulation:
    def __init__(self):
        self.controllerFunc = None
        self.highestOrderDerivFunc = None
        self.ani = None
        self.ax = None
        self.procLine = None
        self.fig = None
        self.order = None
        self.delta_c = None
        self.delta_ysp = None
        self.deadTime = None
        self.delta_yRealList = None
        self.delta_cList = None
        self.delta_ySeenList = None
        self.timeList = None
        self.realDerivListCache = None
        self.seenDerivList = None
        self.realDerivList = None
        self.integrated_error = None
        self.time = None
        self.currentPos = None
        self.deadTimePos = None
        self.noiseSTD = None
        self.controllerOutput = None

    def Reset(self, GUIData=None):
        self.time = 0
        self.integrated_error = 0
        self.controllerOutput = 0
        self.realDerivList = []
        self.seenDerivList = []
        self.realDerivListCache = []
        for i in range(0, derivListSize):
            self.realDerivList.append(0)
            self.seenDerivList.append(0)
        self.realDerivListCache.append(self.realDerivList.copy())

        self.timeList = [0]
        self.delta_ySeenList = [0]
        self.delta_cList = [0]
        self.delta_yRealList = [0]

        self.currentPos = 0
        self.deadTimePos = 0

        if GUIData:
            self.UpdateParams(GUIData)

        self.SetUpGraph()

    def UpdateParams(self, GUIData):
        # General Variables
        delta_yReal = Function("delta_yReal")
        delta_ySeen = Function("delta_ySeen")

        processType = GUIData["ProcessType"]

        # self.timeEnd = GUIData["Duration"]
        self.deadTime = GUIData["Parameters"]["ThetaP"] if GUIData["DeadTimeType"] else 0
        self.noiseSTD = GUIData["NoiseSTD"]

        # Define Controller
        self.delta_ysp = GUIData["SetPointStepChange"]
        delta_e = self.delta_ysp - delta_ySeen(t)
        self.delta_c = 0 * t  # TODO: Kinda Weird
        if GUIData["ControlType"]["pControl"]:
            self.delta_c += Kc * delta_e
        if GUIData["ControlType"]["iControl"]:
            self.delta_c += Kc / Ti * integral_error
        if GUIData["ControlType"]["dControl"]:
            self.delta_c += Kc * Td * diff(delta_e, t)
        self.delta_c = self.delta_c.subs(
            GUIData["Parameters"]
        )
        self.controllerFunc = lambdify([delta_ySeen(t), diff(delta_ySeen(t)), integral_error], self.delta_c, 'numpy')

        # Define Process
        delta_d = GUIData["DisturbanceStepChange"]
        delta_u = Symbol("delta_u")
        if processType == "I":
            ODE = diff(delta_yReal(t), t) - Kp * delta_u - Kd * delta_d
        elif processType == "FO":
            ODE = Tp * diff(delta_yReal(t), t) + 1 * delta_yReal(t) - Kp * delta_u - Kd * delta_d
        elif processType == "SO":
            ODE = (Tn ** 2) * diff(diff(delta_yReal(t), t), t) + 2 * Zeta * Tn * diff(delta_yReal(t), t) + 1 * delta_yReal(t) - Kp * delta_u - Kd * delta_d
        else:
            print(f"Process Type: {processType} is not supported")
            raise ValueError()
        ODE = ODE.subs(
            GUIData["Parameters"]
        )
        lambdas = []
        self.order = ode_order(ODE, delta_yReal(t))
        for i in range(0, self.order):
            lambdas.append(diff(delta_yReal(t), (t, i)))
        lambdas.append(delta_u)
        highestOrderDeriv = solve(ODE, diff(delta_yReal(t), (t, self.order)))[0]
        self.highestOrderDerivFunc = lambdify(lambdas, highestOrderDeriv, 'numpy')

        self.controllerOutput = self.controllerFunc(*self.seenDerivList[0:2], self.integrated_error)
        self.delta_cList[-1] = self.controllerOutput

        self.realDerivList[self.order] = self.highestOrderDerivFunc(*self.realDerivList[0:self.order],self.controllerOutput)
        self.realDerivListCache[-1] = self.realDerivList.copy()


    def GeneratePoint(self):
        # New Time
        self.time += resolution

        # Determine Seen Deriv List
        # DeadTime
        self.currentPos = round(self.time / resolution) - 1
        self.deadTimePos = max(0, self.deadTimePos, self.currentPos - round(self.deadTime / resolution)) - 1
        print(self.deadTimePos)

        # Noise / Generate
        oldList = self.seenDerivList.copy()
        self.seenDerivList = self.realDerivListCache[self.deadTimePos].copy()
        self.seenDerivList[0] += np.random.normal(0, self.noiseSTD)
        for i in range(1, derivListSize):
            self.seenDerivList[i] = (self.seenDerivList[i - 1] - oldList[i - 1]) / resolution

        # Next Step Controller Output
        error = self.delta_ysp - self.seenDerivList[0]
        self.integrated_error += error * resolution
        self.controllerOutput = self.controllerFunc(*self.seenDerivList[0:2], self.integrated_error)

        # Update Real Process. Controller is from last time step
        for i in range(self.order):
            self.realDerivList[i] += self.realDerivList[i + 1] * resolution
        self.realDerivList[self.order] = self.highestOrderDerivFunc(*self.realDerivList[0:self.order], self.controllerOutput)
        self.realDerivListCache.append(self.realDerivList.copy())

        # Update Curves
        self.timeList.append(self.time)
        self.delta_ySeenList.append(self.seenDerivList[0])
        self.delta_yRealList.append(self.realDerivList[0])
        self.delta_cList.append(self.controllerOutput)

    def SetUpGraph(self):
        self.fig, self.ax = plt.subplots()

        self.ax.set_ylim(-10, 10)
        self.procLine, = self.ax.plot([], [], color='green')
        self.ctrlLine, = self.ax.plot([], [], color='orange')
        self.realLine, = self.ax.plot([], [], color='purple')

        self.ani = animation.FuncAnimation(self.fig, self.UpdateGraph, init_func=self.InitGraph, blit=False,
                                           interval=1000 * resolution * chunkSize / speedRatio, cache_frame_data=False)
        plt.show()

    def InitGraph(self):
        self.procLine.set_data([], [])
        self.ctrlLine.set_data([], [])
        self.realLine.set_data([], [])
        return self.procLine, self.ctrlLine, self.realLine

    def UpdateGraph(self, frame):
        listRange = int(windowSize / resolution)

        # Generate Batches of Points
        for i in range(chunkSize):
            self.GeneratePoint()

        self.procLine.set_data(self.timeList[-listRange:], self.delta_ySeenList[-listRange:])
        self.ctrlLine.set_data(self.timeList[-listRange:], self.delta_cList[-listRange:])
        self.realLine.set_data(self.timeList[-listRange:], self.delta_yRealList[-listRange:])
        self.ax.set_xlim(self.time - windowSize, self.time + 1)

        return self.procLine, self.ctrlLine, self.realLine

    def ExportCurve(self):
        df = pd.DataFrame({
            "Time (s)": self.timeList,
            "Output (delta_y)": self.delta_ySeenList,
            "Controller": self.delta_cList,
            "Real PV": self.delta_yRealList
        })
        df.to_excel("simulation_output.xlsx", index=False)
        print("Excel file saved as simulation_output.xlsx")

    # TODO: There is a derivative control discrepancy
    # TODO: order deteriorates if 0 on parameter
    # TODO: Error handling for incorrect entries (Ti = 0)
