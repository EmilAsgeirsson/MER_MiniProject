import numpy as np
import matplotlib.pyplot as plt
import Force_calc

# Generate x values from 0 to 1000 with 0.1 steps
x = np.arange(0, 1000, 1)

# Calculate y values using a mathematical formula
n_cycles = 5
y = abs(90 * np.sin(np.deg2rad(x/(1000/n_cycles)*90)))

pressure = 100
#force = pressure * np.abs(np.gradient(y))

force_arr = np.zeros(len(y))
power_arr = np.zeros(len(y))
# A forloop to calculate the force and power values for each y value
for i in range(len(y)):
    force = Force_calc.calculate_force(y[i], pressure, True)
    force_arr[i] = force
    power = Force_calc.calc_power(y[i], y[i-1], 0.001, pressure, True)
    power_arr[i] = power

data = np.vstack((x, y, force, power)).T

np.savetxt('curve_data2.csv', data, delimiter=',', comments='', fmt='%.1f, %.6f, %.1f, %.1f')

# Plot the curve
plt.plot(x, y, label='Y Value')
plt.plot(x, force, label='Force Value')
plt.xlabel('X Value')
plt.ylabel('Y/Force Value')
plt.title('Continuous Curve and Force Value with X Ranging from 0 to 1000')
plt.grid(True)
plt.show()