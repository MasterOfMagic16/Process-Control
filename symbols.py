from sympy import Symbol, Function

# Define Variables
# Laplace Variables
t = Symbol("t")
s = Symbol("s")

# Standard Form Process Constants:
Kp = Symbol("Kp")  # Steady State Process Gain: (Final Output - Initial Output) / (Final Input - Initial Input)
Tp = Symbol("Tp")  # Time Constant Process: Essentially speed, > 0
Tn = Symbol("Tn")  # 1 / frequency osc rad/sec
Zeta = Symbol("Zeta")  # Damping Factor
ThetaP = Symbol("ThetaP")  # Deadtime

# Standard Form Process Functions
deltay = Function("deltay")  # output as a function of time
deltaY = Symbol("deltaY")
Output = Symbol("deltaOutput")

# Controls
Kc = Symbol("Kc")
Ti = Symbol("Ti")
Td = Symbol("Td")
deltae = Function("deltae")
deltac = Function("deltac")
deltaE = Function("deltaE")
deltaC = Function("deltaC")

