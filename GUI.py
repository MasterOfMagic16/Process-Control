import tkinter as tk
from main import Main

# Root
root = tk.Tk()
root.title('Python Process Control Simulator')
root.geometry('600x400')

# Variable Initialization
Laplace = tk.BooleanVar()

# Process Select Variables
processType = tk.StringVar()
processType.set('FO')
deadTimeType = tk.BooleanVar()

# Process Parameter Variables
KpParam = tk.DoubleVar()
TpParam = tk.DoubleVar()
TnParam = tk.DoubleVar()
ZetaParam = tk.DoubleVar()
ThetaPParam = tk.DoubleVar()

# Controller Select Variables
pControl = tk.BooleanVar()
iControl = tk.BooleanVar()
dControl = tk.BooleanVar()

# Controller Parameter Variables
KcParam = tk.DoubleVar()
TiParam = tk.DoubleVar()
TdParam = tk.DoubleVar()

# Disturbance Parameter Variables
DistStepParam = tk.DoubleVar()
KdParam = tk.DoubleVar()

# SetPoint Parameter Variables
SPStepParam = tk.DoubleVar()

# Get Variable Data
GUIData = {
    "FlatParams": {},
    'ProcessType': "",
    'ControlType': {}
}


def UpdateGUIData():
    GUIData["FlatParams"].update({
        "Kp": KpParam.get(),
        "Tp": TpParam.get(),
        "Zeta": ZetaParam.get(),
        "Tn": TnParam.get(),
        "ThetaP": ThetaPParam.get(),
        "Kc": KcParam.get(),
        "Ti": TiParam.get(),
        "Td": TdParam.get(),
        "Kd": KdParam.get()
    })
    GUIData["ProcessType"] = processType.get()
    GUIData["DeadTimeType"] = deadTimeType.get()
    GUIData["ControlType"].update({
        "pControl": pControl.get(),
        "iControl": iControl.get(),
        "dControl": dControl.get()
    })
    GUIData["DisturbanceStepChange"] = DistStepParam.get()
    GUIData["SetPointStepChange"] = SPStepParam.get()
    GUIData["Laplace"] = Laplace.get()


# Command Functions
def UpdateProcessParamDisplay():
    KpParamFrame.pack_forget()
    TpParamFrame.pack_forget()
    ZetaParamFrame.pack_forget()
    TnParamFrame.pack_forget()
    ThetaPParamFrame.pack_forget()

    KpParamFrame.pack()
    if processType.get() == "FO":
        TpParamFrame.pack()
    elif processType.get() == "SO":
        ZetaParamFrame.pack()
        TnParamFrame.pack()
    if deadTimeType.get():
        ThetaPParamFrame.pack()


def UpdateControlParamDisplay():
    KcParamFrame.pack_forget()
    TiParamFrame.pack_forget()
    TdParamFrame.pack_forget()

    if pControl.get() or iControl.get() or dControl.get():
        KcParamFrame.pack()
    if iControl.get():
        TiParamFrame.pack()
    if dControl.get():
        TdParamFrame.pack()


def Activate():
    UpdateGUIData()
    Main(GUIData)


# Frames / Visuals
# Process Config Frame
processConfigFrame = tk.Frame(root, borderwidth=2, relief='groove')
processConfigFrame.grid(row=0, column=0, sticky='nw')

# Process Select Frame
processSelectFrame = tk.Frame(processConfigFrame)
processSelectFrame.grid(row=0, column=0)
tk.Label(processSelectFrame, text='Process Type:').pack()
tk.Radiobutton(processSelectFrame, text="Integrating", variable=processType, value='I', command=UpdateProcessParamDisplay).pack()
tk.Radiobutton(processSelectFrame, text="First Order", variable=processType, value='FO', command=UpdateProcessParamDisplay).pack()
tk.Radiobutton(processSelectFrame, text="Second Order", variable=processType, value='SO', command=UpdateProcessParamDisplay).pack()
tk.Checkbutton(processSelectFrame, text='Deadtime?', variable=deadTimeType, command=UpdateProcessParamDisplay).pack()

# Process Parameter Frame
processParameterFrame = tk.Frame(processConfigFrame)
processParameterFrame.grid(row=0, column=1, sticky='n')
tk.Label(processParameterFrame, text='Process Parameters:', anchor='n').pack()

KpParamFrame = tk.Frame(processParameterFrame)
tk.Label(KpParamFrame, text='Kp:').grid(row=0, column=0)
tk.Entry(KpParamFrame, textvariable=KpParam, justify='center').grid(row=0, column=1)

TpParamFrame = tk.Frame(processParameterFrame)
tk.Label(TpParamFrame, text='Tp:').grid(row=0, column=0)
tk.Entry(TpParamFrame, textvariable=TpParam, justify='center').grid(row=0, column=1)

ZetaParamFrame = tk.Frame(processParameterFrame)
tk.Label(ZetaParamFrame, text='Zeta:').grid(row=0, column=0)
tk.Entry(ZetaParamFrame, textvariable=ZetaParam, justify='center').grid(row=0, column=1)

TnParamFrame = tk.Frame(processParameterFrame)
tk.Label(TnParamFrame, text='Tn:').grid(row=0, column=0)
tk.Entry(TnParamFrame, textvariable=TnParam, justify='center').grid(row=0, column=1)

ThetaPParamFrame = tk.Frame(processParameterFrame)
tk.Label(ThetaPParamFrame, text='ThetaP:').grid(row=0, column=0)
tk.Entry(ThetaPParamFrame, textvariable=ThetaPParam, justify='center').grid(row=0, column=1)

UpdateProcessParamDisplay()


# Controller Config
controlConfigFrame = tk.Frame(root, borderwidth=2, relief='groove')
controlConfigFrame.grid(row=1, column=0, sticky='nw')

# Controller Select Frame
controlSelectFrame = tk.Frame(controlConfigFrame)
controlSelectFrame.grid(row=0, column=0)
tk.Label(controlSelectFrame, text='Controller Type:').pack()
tk.Checkbutton(controlSelectFrame, text='Proportional', variable=pControl, command=UpdateControlParamDisplay).pack()
tk.Checkbutton(controlSelectFrame, text='Integral', variable=iControl, command=UpdateControlParamDisplay).pack()
tk.Checkbutton(controlSelectFrame, text='Derivative', variable=dControl, command=UpdateControlParamDisplay).pack()

# Controller Parameter Frame
controlParameterFrame = tk.Frame(controlConfigFrame)
controlParameterFrame.grid(row=0, column=1, sticky='n')
tk.Label(controlParameterFrame, text='Controller Parameters:', anchor='n').pack()

KcParamFrame = tk.Frame(controlParameterFrame)
tk.Label(KcParamFrame, text='Kc:').grid(row=0, column=0)
tk.Entry(KcParamFrame, textvariable=KcParam, justify='center').grid(row=0, column=1)

TiParamFrame = tk.Frame(controlParameterFrame)
tk.Label(TiParamFrame, text='Ti:').grid(row=0, column=0)
tk.Entry(TiParamFrame, textvariable=TiParam, justify='center').grid(row=0, column=1)

TdParamFrame = tk.Frame(controlParameterFrame)
tk.Label(TdParamFrame, text='Td:').grid(row=0, column=0)
tk.Entry(TdParamFrame, textvariable=TdParam, justify='center').grid(row=0, column=1)

UpdateControlParamDisplay()


# Disturbance Frame
DisturbanceFrame = tk.Frame(root, borderwidth=2, relief='groove')
DisturbanceFrame.grid(row=2, sticky='nw')

DistStepParamFrame = tk.Frame(DisturbanceFrame)
DistStepParamFrame.grid(row=0, column=0)
tk.Label(DistStepParamFrame, text='Disturbance Step Change: ').grid(row=0, column=0)
tk.Entry(DistStepParamFrame, textvariable=DistStepParam, justify='center').grid(row=1, column=0)

KdParamFrame = tk.Frame(DisturbanceFrame)
KdParamFrame.grid(row=0, column=1)
tk.Label(KdParamFrame, text='Kd:').grid(row=0, column=0)
tk.Entry(KdParamFrame, textvariable=KdParam, justify='center').grid(row=1, column=0)

# SetPoint Frame
SetPointFrame = tk.Frame(root, borderwidth=2, relief='groove')
SetPointFrame.grid(row=3, sticky='nw')

SPStepParamFrame = tk.Frame(SetPointFrame)
SPStepParamFrame.grid(row=0, column=0)
tk.Label(SPStepParamFrame, text='SetPoint Step Change:').grid(row=0, column=0)
tk.Entry(SPStepParamFrame, textvariable=SPStepParam, justify='center').grid(row=1, column=0)


# Activation Button
activateButton = tk.Button(root, text='Activate', command=Activate)
activateButton.grid(row=4, sticky='nw')

modeSwitch = tk.Checkbutton(root, text='Laplace On', variable=Laplace)
modeSwitch.grid(row=5, sticky='n')

# Loop Root
root.mainloop()


