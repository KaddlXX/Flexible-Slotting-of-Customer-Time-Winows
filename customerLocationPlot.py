import matplotlib.pyplot as plt
import v1
import utils.calculateDistance as cd


customerList = readData.test()

plt.scatter(x=[int(customer.xCoord) for customer in customerList], y=[int(customer.yCoord) for customer in customerList])
plt.xlabel('x_values')
plt.ylabel('y_values')
plt.show()

for customer in customerList:
    print(cd.computeDistance([int(customer.xCoord), int(customer.yCoord)], [10,10]))
