import numpy as np
import matplotlib.pyplot as plt

# Generate x values from 0 to 1000 with 0.1 steps
x = np.arange(0, 1000, 1)

# Calculate y values using a mathematical formula
n_cycles = 5
y = abs(90 * np.sin(np.deg2rad(x/(1000/n_cycles)*90)))

pressure = 100
force = pressure * np.abs(np.gradient(y))

data = np.vstack((x, y, force)).T

np.savetxt('curve_data.csv', data, delimiter=',', comments='', fmt='%.1f, %.6f, %.1f')

# Plot the curve
plt.plot(x, y, label='Y Value')
plt.plot(x, force, label='Force Value')
plt.xlabel('X Value')
plt.ylabel('Y/Force Value')
plt.title('Continuous Curve and Force Value with X Ranging from 0 to 1000')
plt.grid(True)
plt.show()