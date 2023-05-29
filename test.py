import numpy as np
import matplotlib.pyplot as plt
import Force_calc
import math

length_rod = 755 # mm
ang = 55
start = length_rod * math.cos(math.radians(ang))
y_values_stroke = length_rod * math.cos(math.radians(ang)) * -1
print(y_values_stroke + start)

ang = 115
y_values_stroke = length_rod * math.cos(math.radians(ang)) * -1
print(y_values_stroke + start )