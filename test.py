import random
import numpy as np
import matplotlib.pyplot as plt
result = []
N = 200
p = 2/3
startCond = 3
xk = startCond
rounds = 10000

roundResult = np.zeros(rounds)
endResult = []

for i in range(1, 10):
    startCond = i
    for i in range(rounds):
        
        while xk > 0 and xk < N:# breaking condition
            output = random.random()

            if p > output:
                # print("increased xk: ", xk)
                xk = xk + 1
            else:
                # print("decreased xk: ", xk)
                xk = xk - 1


            if xk == 0:
                roundResult[i] = 0
                # print(result)

            if xk == N:
                roundResult[i] = 1
                # print(result)

        xk = startCond

    endResult.append(sum(roundResult)/len(roundResult))


plt.plot(np.arange(1,10,1), endResult)





