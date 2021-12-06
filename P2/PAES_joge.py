from platypus import PAES, ZDT1, ZDT2, ZDT3, ZDT4, ZDT5, ZDT6
import matplotlib.pyplot as plt

# define the problem definition
problem = ZDT5()

# instantiate the optimization algorithm
algorithm = PAES(problem)

# optimize the problem using 10,000 function evaluations
algorithm.run(10000)

# display and store the results
x = []
y = []
for solution in algorithm.result:
    print(solution.objectives)
    x.append(solution.objectives[0])
    y.append(solution.objectives[1])

# plot the results
plt.scatter(x,y)
plt.show()
    