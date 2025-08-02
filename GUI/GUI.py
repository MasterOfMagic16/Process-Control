import tkinter as tk
from GUIVars import GUIVars
from main import Main

# Root
root = tk.Tk()
root.title('Python Process Control Simulator')
root.geometry('620x350')
root.resizable(False, False)

# Variable Tracker
guiVars = GUIVars()


# Frames / Visuals
# Process Config Frame Update
def UpdateProcessConfigFrame():
    KpParamFrame.pack_forget()
    TpParamFrame.pack_forget()
    ZetaParamFrame.pack_forget()
    TnParamFrame.pack_forget()
    ThetaPParamFrame.pack_forget()

    KpParamFrame.pack(anchor='e', pady=2)
    if guiVars.processType.get() == "FO":
        TpParamFrame.pack(anchor='e', pady=2)
    elif guiVars.processType.get() == "SO":
        ZetaParamFrame.pack(anchor='e', pady=2)
        TnParamFrame.pack(anchor='e', pady=2)
    if guiVars.deadTimeType.get():
        ThetaPParamFrame.pack(anchor='e', pady=2)


# Process Config Frame
processConfigFrame = tk.LabelFrame(root, text="Process", width=300, height=150, borderwidth=2, relief='groove')
processConfigFrame.grid_propagate(False)
processConfigFrame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

# Process Select Frame
processSelectFrame = tk.Frame(processConfigFrame, width=100, height=125, borderwidth=2, relief='groove')
processSelectFrame.pack_propagate(False)
processSelectFrame.grid(row=0, column=0, padx=5, sticky='nsew')
tk.Label(processSelectFrame, text='Process Type:').pack(anchor='w')
tk.Radiobutton(processSelectFrame, text="Integrating", variable=guiVars.processType, value='I', command=UpdateProcessConfigFrame).pack(anchor='w')
tk.Radiobutton(processSelectFrame, text="First Order", variable=guiVars.processType, value='FO', command=UpdateProcessConfigFrame).pack(anchor='w')
tk.Radiobutton(processSelectFrame, text="Second Order", variable=guiVars.processType, value='SO', command=UpdateProcessConfigFrame).pack(anchor='w')
tk.Checkbutton(processSelectFrame, text='DeadTime?', variable=guiVars.deadTimeType, command=UpdateProcessConfigFrame).pack(anchor='w')

# Process Parameter Frame
processParameterFrame = tk.Frame(processConfigFrame, width=180, borderwidth=2, relief='groove')
processParameterFrame.pack_propagate(False)
processParameterFrame.grid(row=0, column=1, sticky='nsew')
tk.Label(processParameterFrame, text='Process Parameters:').pack(anchor='e', pady=1)

KpParamFrame = tk.Frame(processParameterFrame)
tk.Label(KpParamFrame, text='Kp:').grid(row=0, column=0)
tk.Entry(KpParamFrame, textvariable=guiVars.KpParam, justify='center').grid(row=0, column=1)

TpParamFrame = tk.Frame(processParameterFrame)
tk.Label(TpParamFrame, text='Tp:').grid(row=0, column=0)
tk.Entry(TpParamFrame, textvariable=guiVars.TpParam, justify='center').grid(row=0, column=1)

ZetaParamFrame = tk.Frame(processParameterFrame)
tk.Label(ZetaParamFrame, text='Zeta:').grid(row=0, column=0)
tk.Entry(ZetaParamFrame, textvariable=guiVars.ZetaParam, justify='center').grid(row=0, column=1)

TnParamFrame = tk.Frame(processParameterFrame)
tk.Label(TnParamFrame, text='Tn:').grid(row=0, column=0)
tk.Entry(TnParamFrame, textvariable=guiVars.TnParam, justify='center').grid(row=0, column=1)

ThetaPParamFrame = tk.Frame(processParameterFrame)
tk.Label(ThetaPParamFrame, text='ThetaP:').grid(row=0, column=0)
tk.Entry(ThetaPParamFrame, textvariable=guiVars.ThetaPParam, justify='center').grid(row=0, column=1)

UpdateProcessConfigFrame()


# Control Config Frame Update
def UpdateControlConfigFrame():
    KcParamFrame.pack_forget()
    TiParamFrame.pack_forget()
    TdParamFrame.pack_forget()

    if guiVars.pControl.get() or guiVars.iControl.get() or guiVars.dControl.get():
        KcParamFrame.pack(anchor='e', pady=2)
    if guiVars.iControl.get():
        TiParamFrame.pack(anchor='e', pady=2)
    if guiVars.dControl.get():
        TdParamFrame.pack(anchor='e', pady=2)


# Controller Config Frame
controlConfigFrame = tk.LabelFrame(root, text="Controller", width=300, height=150, borderwidth=2, relief='groove')
controlConfigFrame.grid_propagate(False)
controlConfigFrame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

# Controller Select Frame
controlSelectFrame = tk.Frame(controlConfigFrame, width=100, height=125, borderwidth=2, relief='groove')
controlSelectFrame.pack_propagate(False)
controlSelectFrame.grid(row=0, column=0, padx=5, sticky='nsew')
tk.Label(controlSelectFrame, text='Controller Type:').pack()
tk.Checkbutton(controlSelectFrame, text='Proportional', variable=guiVars.pControl, command=UpdateControlConfigFrame).pack(anchor='w')
tk.Checkbutton(controlSelectFrame, text='Integral', variable=guiVars.iControl, command=UpdateControlConfigFrame).pack(anchor='w')
tk.Checkbutton(controlSelectFrame, text='Derivative', variable=guiVars.dControl, command=UpdateControlConfigFrame).pack(anchor='w')

# Controller Parameter Frame
controlParameterFrame = tk.Frame(controlConfigFrame, width=185, height=125, borderwidth=2, relief='groove')
controlParameterFrame.pack_propagate(False)
controlParameterFrame.grid(row=0, column=1, sticky='nsew')
tk.Label(controlParameterFrame, text='Controller Parameters:').pack(anchor='e', pady=1)

KcParamFrame = tk.Frame(controlParameterFrame)
tk.Label(KcParamFrame, text='Kc:').grid(row=0, column=0, sticky='e')
tk.Entry(KcParamFrame, textvariable=guiVars.KcParam, justify='center').grid(row=0, column=1)

TiParamFrame = tk.Frame(controlParameterFrame)
tk.Label(TiParamFrame, text='Ti:').grid(row=0, column=0)
tk.Entry(TiParamFrame, textvariable=guiVars.TiParam, justify='center').grid(row=0, column=1)

TdParamFrame = tk.Frame(controlParameterFrame)
tk.Label(TdParamFrame, text='Td:').grid(row=0, column=0)
tk.Entry(TdParamFrame, textvariable=guiVars.TdParam, justify='center').grid(row=0, column=1)

UpdateControlConfigFrame()


# Disturbance Frame
DisturbanceFrame = tk.LabelFrame(root, width=300, height=75, text="Disturbance", borderwidth=2, relief='groove')
DisturbanceFrame.grid_propagate(False)
DisturbanceFrame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

DistStepParamFrame = tk.Frame(DisturbanceFrame, width=130, height=50, borderwidth=2, relief='groove')
DistStepParamFrame.grid_propagate(False)
DistStepParamFrame.grid(row=0, column=0, padx=5)
tk.Label(DistStepParamFrame, text='Step Change: ').grid(row=0, column=0)
tk.Entry(DistStepParamFrame, textvariable=guiVars.DistStepParam, justify='center').grid(row=1, column=0)

KdParamFrame = tk.Frame(DisturbanceFrame, width=130, height=50, borderwidth=2, relief='groove')
KdParamFrame.grid_propagate(False)
KdParamFrame.grid(row=0, column=1, padx=15, sticky='e')
tk.Label(KdParamFrame, text='Kd:').grid(row=0, column=0)
tk.Entry(KdParamFrame, textvariable=guiVars.KdParam, justify='center').grid(row=1, column=0)


# SetPoint Frame
SetPointFrame = tk.LabelFrame(root, text="Set Point", width=300, height=75, borderwidth=2, relief='groove')
SetPointFrame.grid_propagate(False)
SetPointFrame.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

SPStepParamFrame = tk.Frame(SetPointFrame, width=130, height=50, borderwidth=2, relief='groove')
SPStepParamFrame.grid_propagate(False)
SPStepParamFrame.grid(row=0, padx=85)
tk.Label(SPStepParamFrame, text='Step Change:').grid(row=0, column=0)
tk.Entry(SPStepParamFrame, textvariable=guiVars.SPStepParam, justify='center').grid(row=1)


# Simulation Frame
SimulationFrame = tk.LabelFrame(root, text='Simulation', width=185, height=100, borderwidth=2, relief='groove')
SimulationFrame.grid_propagate(False)
SimulationFrame.grid(row=2, columnspan=2)

StepSizeFrame = tk.Frame(SimulationFrame)
tk.Label(SimulationFrame, text='Step Size:').grid(row=0, column=0)
tk.Entry(SimulationFrame, textvariable=guiVars.stepSize, justify='center').grid(row=0, column=1)

DurationFrame = tk.Frame(SimulationFrame)
tk.Label(SimulationFrame, text='Duration:').grid(row=1, column=0)
tk.Entry(SimulationFrame, textvariable=guiVars.duration, justify='center').grid(row=1, column=1)

# GO Button
def RunSimulation():
    Main(guiVars.GetData())


tk.Button(SimulationFrame, text='Run Simulation', command=RunSimulation).grid(row=2, columnspan=2, padx=5, pady=5)


# Loop Root
root.mainloop()
