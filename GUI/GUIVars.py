import tkinter as tk


class GUIVars:
    def __init__(self):
        # Simulation Variables
        self.stepSize = tk.DoubleVar()
        self.stepSize.set(.001)
        self.duration = tk.DoubleVar()
        self.duration.set(10)

        # Process Select Variables
        self.processType = tk.StringVar()
        self.processType.set('FO')
        self.deadTimeType = tk.BooleanVar()

        # Process Parameter Variables
        self.KpParam = tk.DoubleVar()
        self.TpParam = tk.DoubleVar()
        self.TnParam = tk.DoubleVar()
        self.ZetaParam = tk.DoubleVar()
        self.ThetaPParam = tk.DoubleVar()

        # Controller Select Variables
        self.pControl = tk.BooleanVar()
        self.iControl = tk.BooleanVar()
        self.dControl = tk.BooleanVar()

        # Controller Parameter Variables
        self.KcParam = tk.DoubleVar()
        self.TiParam = tk.DoubleVar()
        self.TdParam = tk.DoubleVar()

        # Disturbance Parameter Variables
        self.DistStepParam = tk.DoubleVar()
        self.KdParam = tk.DoubleVar()

        # SetPoint Parameter Variables
        self.SPStepParam = tk.DoubleVar()

    def GetData(self):
        GUIData = {
            "Parameters": {
                "Kp": self.KpParam.get(),
                "Tp": self.TpParam.get(),
                "Zeta": self.ZetaParam.get(),
                "Tn": self.TnParam.get(),
                "ThetaP": self.ThetaPParam.get(),
                "Kc": self.KcParam.get(),
                "Ti": self.TiParam.get(),
                "Td": self.TdParam.get(),
                "Kd": self.KdParam.get()
                },
            "ProcessType": self.processType.get(),
            "DeadTimeType": self.deadTimeType.get(),
            "ControlType": {
                "pControl": self.pControl.get(),
                "iControl": self.iControl.get(),
                "dControl": self.dControl.get()
                },
            "DisturbanceStepChange": self.DistStepParam.get(),
            "SetPointStepChange": self.SPStepParam.get(),
            "StepSize": self.stepSize.get(),
            "Duration": self.duration.get()
        }

        return GUIData
