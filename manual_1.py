import statistics
import numpy as np
import matplotlib.pyplot as plt
cdf = lambda x: ((x-900)/100)**2
x = np.linspace(905,1000,96)
y = np.linspace(930,1000,71)
pmf = lambda x: (2*(x-900)/100)
profit = lambda x, y: (cdf(x)*(1000-x))+((cdf(y)-cdf(x))*(1000-y))
#plt.plot(x,pmf(x))
profits = []
prev_y_profit = 0
for step in x:
    for stepped in y:
        curr_prof = profit(step, stepped)
        profits.append([step,stepped, curr_prof])
       # if prev_y_profit > curr_prof:
       #     prev_y_profit = 0
       #     break
       # prev_y_profit = curr_prof
max_profit = [0,0,0]
for trade in profits:
    print(trade)
    if trade[2] > max_profit[2]:
        max_profit = trade
print(f"x: {max_profit[0]}, y: {max_profit[1]}, profit: {max_profit[2]}")



