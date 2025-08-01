from sympy import Symbol, Function

# Process Parameters
Kp = Symbol("Kp")  # Steady State Process Gain: (Final Output - Initial Output) / (Final Input - Initial Input)
Tp = Symbol("Tp")  # Time Constant Process: Essentially speed, > 0
Tn = Symbol("Tn")  # 1 / frequency osc rad/sec
Zeta = Symbol("Zeta")  # Damping Factor
ThetaP = Symbol("ThetaP")  # DeadTime

# Disturbance Parameters
Kd = Symbol("Kd")

# Controls Parameters
integral_error = Symbol("integrated_error")
Kc = Symbol("Kc")
Ti = Symbol("Ti")
Td = Symbol("Td")

# Laplace Variables
t = Symbol("t")
s = Symbol("s")
