import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import csv
from PIL import Image, ImageTk
from time import sleep
import sys
import signal
import math
import atexit
import Force_calc

## ADD POWER AS GRAPH OR JUST NUMBER?
BOOL_ENCODER = False

if BOOL_ENCODER:
    from Encoder.scripts.encoder import Encoder
# Check if any ports is installed:
    ports = Encoder.check_for_COM()
    if len(ports) == 0:
        sys.exit(1)
    
    # Define encoder
    encoder = Encoder(port="COM3")

# Define the update interval in milliseconds
UPDATE_INTERVAL = 1
# data list
DATA = []

def signal_handler():
    '''
    Signal handler. Detects program interrupts and stops motors before halting program.
    '''
    if BOOL_ENCODER:
        encoder.end_thread()
        print("thread ended")    
        sleep(1)
    print('program ended')
    sys.exit(1)

# Set up signal handler
atexit.register(signal_handler)

# Create the Tkinter GUI window
root = tk.Tk()
root.title("Sensor Data Graph")
root.geometry("1920x600")
root.configure(bg='#FFFFFF')

# Create canvas to make distinct cololors
canvas_side = tk.Canvas(master=root, width=100, height=1080, bg='#365274', borderwidth=0, highlightthickness=0)
canvas_top = tk.Canvas(master=root, width=1920, height=100, bg='#18315A', borderwidth=0, highlightthickness=0)
canvas_topleft = tk.Canvas(master=root, width=100, height=100, bg='#FFFFFF', borderwidth=0, highlightthickness=0)
canvas_side.place(x=0,y=0)
canvas_top.place(x=0,y=0)
canvas_topleft.place(x=0,y=0)

# Add logo
# Load the image file using Pillow
pil_image = Image.open("SDU_BLACK_RGB_png.png")
resize = pil_image.resize([90,25])
#827x221
# Convert the PIL Image object to a Tkinter PhotoImage object
tk_image = ImageTk.PhotoImage(resize)

# Add the image to the canvas at position (0, 0)
canvas_logo = tk.Canvas(master=root, width=95, height=25, bg='#FFFFFF', borderwidth=0, highlightthickness=0)
canvas_logo.create_image(5, 0, anchor=tk.NW, image=tk_image)
canvas_logo.place(x=0,y=37)

########### SENSOR PLOT ###########

# Create a Matplotlib figure and plot the initial data
fig_ang_sens = Figure(figsize=(6, 4), dpi=100)
ax_ang_sens = fig_ang_sens.add_subplot(111)
line_ang_sens, = ax_ang_sens.plot([], [])
ax_ang_sens.set_xlabel('Time (s)')
ax_ang_sens.set_ylabel('Sensor Reading')
ax_ang_sens.set_title('Sensor Data')
ax_ang_sens.set_yticks([0, 45, 90, 135, 180, 225, 270])
y_min = 0
y_max = 300
ax_ang_sens.set_ylim(y_min, y_max)

# Create a canvas to display the Matplotlib figure
canvas_sensor_ang_plot = FigureCanvasTkAgg(fig_ang_sens, master=root)
canvas_sensor_ang_plot.draw()
canvas_sensor_ang_plot.get_tk_widget().place(x=120, y=120)

########### FORCE PLOT ###########
fig_force = Figure(figsize=(6, 4), dpi=100)
ax_force = fig_force.add_subplot(111)
line_force, = ax_force.plot([], [])
ax_force.set_xlabel('Time (s)')
ax_force.set_ylabel('Force (N)')
ax_force.set_title('Force')
#ax_force.set_yticks([0, 45, 90])
y_min = 0#min(y_values)
y_max = 90#max(y_values)
ax_force.set_ylim(y_min, y_max)

# Create a canvas to display the Matplotlib figure
canvas_force_plot = FigureCanvasTkAgg(fig_force, master=root)
canvas_force_plot.draw()
canvas_force_plot.get_tk_widget().place(x=720, y=120)

########### STROKE PLOT ###########
fig_stroke = Figure(figsize=(6, 4), dpi=100)
ax_stroke = fig_stroke.add_subplot(111)
line_stroke, = ax_stroke.plot([], [])
ax_stroke.set_xlabel('Time (s)')
ax_stroke.set_ylabel('Length (mm))')
ax_stroke.set_title('Stroke')
#ax_stroke.set_yticks([0, 45, 90, 135, 180, 225, 270])
y_min = 0#min(y_values)
y_max = 1000#max(y_values)
ax_stroke.set_ylim(y_min, y_max)

# Create a canvas to display the Matplotlib figure
canvas_stroke_plot = FigureCanvasTkAgg(fig_stroke, master=root)
canvas_stroke_plot.draw()
canvas_stroke_plot.get_tk_widget().place(x=1320, y=120)

# Start thread to read data
if BOOL_ENCODER:
    encoder.start_thread()
    count = 0

# Read data from CSV file
def read_data():
    if BOOL_ENCODER:
        DATA.append(encoder.get_data()[0])
        x_values = [float(row["Time"]) for row in DATA]
        x_values = range(len(x_values))
        y_values_senser_ang = [float(row["A2"]) for row in DATA]
        size = int(slider.get())
        line_ang_sens.set_xdata(x_values)
        line_ang_sens.set_ydata(y_values_senser_ang)
    else:
        with open('curve_data.csv', 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        ##### Sensor data #####
        x_values = [float(row[0]) for row in data]
        y_values_senser_ang = [float(row[1]) for row in data]
        size = int(slider.get())
        line_ang_sens.set_xdata(x_values)
        line_ang_sens.set_ydata(y_values_senser_ang)

        ##### Stroke data #####
        length_rod = 800 # mm
        y_values_stroke = [length_rod * math.sin(math.radians(float(row[1]))) for row in data]
        line_stroke.set_xdata(x_values)
        line_stroke.set_ydata(y_values_stroke)

        ##### Force data #####
        y_values_force = [float(row[2]) for row in data]
        #Force_calc.calculate_force_and_power(y_values_senser_ang, )
        line_force.set_xdata(x_values)
        line_force.set_ydata(y_values_force)
    
    # set the limits of the x-axis for sensor, force, and stroke plots 
    x_min = (len(x_values)-size)
    if x_min < 0:
        x_min = 0
    x_max = len(x_values)
    ax_ang_sens.set_xlim(x_min, x_max)
    ax_force.set_xlim(x_min, x_max)
    ax_stroke.set_xlim(x_min, x_max)
    
    # Set auto-scaling for y-axis
    ax_ang_sens.autoscale_view(True,True,True)
    ax_force.autoscale_view(True,True,True)
    ax_stroke.autoscale_view(True,True,True)
    
    # Update the plot
    canvas_sensor_ang_plot.draw()
    canvas_stroke_plot.draw()
    canvas_force_plot.draw()

# Update the data at the specified interval
def update_data():
    read_data()
    root.after(UPDATE_INTERVAL, update_data)

# Create a button to manually update the data
def update_button():
    run_sensor = not run_sensor

# Create a button widget
button = tk.Button(master=root, text="Update Data", command=update_button)
button.place(x=15, y=120)


# Create a Label widget for the text
#style = ttk.Style()
#style.configure("TScale", troughrelief="flat", sliderrelief="flat", sliderthickness=20, troughcolor="lightgray", sliderlength=30)
label = tk.Label(root, text="Use slider to adjust size of displayed data")
label.place(x=950, y=30)
# create a slider widget to adjust the point size
slider = tk.Scale(master=root, from_=1, to=1000, orient=tk.HORIZONTAL)
slider.set(1000) # set initial value
slider.place(x=1000, y=50)

# Start the update loop
update_data()

# Run the Tkinter event loop
tk.mainloop()
