import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import csv
from PIL import Image, ImageTk, ImageGrab, ImageDraw
from time import sleep
import math
import atexit
import Force_calc
from Encoder.scripts.encoder import Encoder


################ HOW TO RUN ################

# 1. Insert the Arduino USB in the laptop
# 2. Find the COM port of the Arduino
# 3. Ensure BOOL_ENCODER is set to True
# 4. Run the program

# Note: You need to remove the USB in order to stop the thread running to the arduino

############################################


BOOL_ENCODER = True

if BOOL_ENCODER:
    # Define encoder
    encoder = Encoder(port="COM4")

# Define the update interval in milliseconds
UPDATE_INTERVAL = 200
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

# Set up signal handler
atexit.register(signal_handler)

# Create the Tkinter GUI window
root = tk.Tk()
root.geometry("1300x950")
root.geometry(f"+0+0")
root.configure(bg='#FFFFFF')
root.title("Exercise equipment with pneumatic resistance")

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
line_ang_sens, = ax_ang_sens.plot([], [], label='Angle')
ax_ang_sens.set_xlabel('Time (s)')
ax_ang_sens.set_ylabel('Angle (deg)')
ax_ang_sens.set_title('Angle Sensor Data')
ax_ang_sens.set_yticks([10 * 1 * i for i in range(5, 13, 1)])
ax_ang_sens.grid(True)
y_min = 50
y_max = 130
ax_ang_sens.set_ylim(y_min, y_max)
ax_ang_sens.legend(loc='upper left')

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
ax_force.grid(True)
ax_force.set_yticks([50 * 1 * i for i in range(10)])
y_min = 0
y_max = 500
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
ax_stroke.set_ylabel('Length (mm)')
ax_stroke.set_title('Stroke')
ax_stroke.grid(True)
ax_stroke.set_yticks([100 * 1 * i for i in range(9)])
y_min = 0
y_max = 850
ax_stroke.set_ylim(y_min, y_max)

# Create a canvas to display the Matplotlib figure
canvas_stroke_plot = FigureCanvasTkAgg(fig_stroke, master=root)
canvas_stroke_plot.draw()
canvas_stroke_plot.get_tk_widget().place(x=120, y=520)

########### POWER PLOT ###########
fig_power = Figure(figsize=(6, 4), dpi=100)
ax_power = fig_power.add_subplot(111)
line_power, = ax_power.plot([], [])
ax_power.set_xlabel('Time (s)')
ax_power.set_ylabel('Power (Watt)')
ax_power.set_title('Power')
ax_power.grid(True)
#ax_power.set_yticks([0, 50, 100, 150, 200, 250, 300])
y_min = -1000
y_max = 1000
ax_power.set_ylim(y_min, y_max)

# Create a canvas to display the Matplotlib figure
canvas_power_plot = FigureCanvasTkAgg(fig_power, master=root)
canvas_power_plot.draw()
canvas_power_plot.get_tk_widget().place(x=720, y=520)

# Start thread to read data
if BOOL_ENCODER:
    encoder.start_thread()
    count = 0

y_values_power = []
y_values_force = []
work = 0
pressure = 0
length_rod = 755 # mm
start_ang = 55 # deg
start_stroke = length_rod * math.cos(math.radians(start_ang))

def read_data():
    global y_values_force, y_values_power, work, pressure, length_rod, start_stroke
    if BOOL_ENCODER:
        data:list = encoder.get_data()
        if len(data) == 0:
            return
        #data[0]["A0"] = 6.0
        DATA.append(data[0])
        
        x_values = [float(row["Time"]) for row in DATA]
        y_values_sensor_ang = [float(row["A2"]) for row in DATA]
        y_values_sensor_pressure = [float(row["A0"]) for row in DATA]
        line_ang_sens.set_xdata(x_values)
        line_ang_sens.set_ydata(y_values_sensor_ang)
        
        # Set global pressure variable
        pressure = y_values_sensor_pressure[-1]

        ##### Stroke data #####
        y_values_stroke = [(length_rod * math.cos(math.radians(ang)) * -1) + start_stroke for ang in y_values_sensor_ang]
        line_stroke.set_xdata(x_values)
        line_stroke.set_ydata(y_values_stroke)

        ##### Force data #####
        force_calc = Force_calc.calculate_force(y_values_sensor_ang[-1], y_values_sensor_pressure[-1], True)
        if math.isnan(force_calc):
            force_calc = 0
        y_values_force.append(force_calc)
        line_force.set_xdata(x_values)
        line_force.set_ydata(y_values_force)

        ##### Power data #####
        if len(y_values_sensor_ang) < 2:
            work, power = 0,0
        else:
            work, power = Force_calc.calc_power(y_values_sensor_ang[-1], y_values_sensor_ang[-2], UPDATE_INTERVAL/1000, y_values_sensor_pressure[-1], True)
        if math.isnan(power):
            power = 0
        if math.isnan(work):
            work = 0

        y_values_power.append(power)
        line_power.set_xdata(x_values)
        line_power.set_ydata(y_values_power)

    else:
        with open('curve_data.csv', 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        ##### Sensor data #####
        x_values = [float(row[0]) for row in data]
        y_values_sensor_ang = [float(row[1]) for row in data]
        size = int(slider.get())
        line_ang_sens.set_xdata(x_values)
        line_ang_sens.set_ydata(y_values_sensor_ang)

        ##### Stroke data #####
        length_rod = 755 # mm
        y_values_stroke = [(length_rod * math.cos(math.radians(float(row[1]))) * -1) + start_stroke for row in data]
        line_stroke.set_xdata(x_values)
        line_stroke.set_ydata(y_values_stroke)

        ##### Force data #####
        y_values_force = [float(row[2]) for row in data]        
        line_force.set_xdata(x_values)
        line_force.set_ydata(y_values_force)

        ##### Power data #####
        y_values_power = [100.0 for _ in range(len(data))]
        line_power.set_xdata(x_values)
        line_power.set_ydata(y_values_power)
    
    # set the limits of the x-axis for sensor, force, and stroke plots 
    size = int(slider.get())
    x_min = min(x_values)
    x_max = max(x_values)
    if x_max > size:
        x_min = x_max - size
    ax_ang_sens.set_xlim(x_min, x_max)
    ax_force.set_xlim(x_min, x_max)
    ax_stroke.set_xlim(x_min, x_max)
    ax_power.set_xlim(x_min, x_max)
    
    # Set auto-scaling for y-axis
    ax_ang_sens.autoscale_view(True,True,True)
    ax_force.autoscale_view(True,True,True)
    ax_stroke.autoscale_view(True,True,True)
    ax_power.autoscale_view(True,True,True)
    
    # Update the plot
    canvas_sensor_ang_plot.draw()
    canvas_stroke_plot.draw()
    canvas_force_plot.draw()
    canvas_power_plot.draw()

# Update the data at the specified interval
def update_data():
    read_data()
    update_power_label()
    root.after(UPDATE_INTERVAL, update_data)

# Create a button to manually update the data
def update_button():
    run_sensor = not run_sensor

def export_ui():
    # Capture a screenshot of the Tkinter window
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    width = root.winfo_width()
    height = root.winfo_height()
    screenshot = ImageGrab.grab((x, y, x + width, y + height))
    
    # Add a thin border line to the screenshot
    border_width = 0.1  # Adjust the border width as desired
    border_color = (0, 0, 0)  # Adjust the border color as desired
    draw = ImageDraw.Draw(screenshot)
    draw.rectangle([(border_width, border_width), (width - border_width - 1, height - border_width - 1)],
                   outline=border_color)
    
    # Save the screenshot as a PNG image
    screenshot.save("ui_screenshot.png", "PNG")
    print("UI screenshot saved.")

def update_power_label():
    global work, pressure 
    # Update the label text
    #label_work.config(text=f'{str(work)} work')
    label_work.config(text=f'{pressure} BAR')
    
    # Schedule the next update
    root.after(UPDATE_INTERVAL, update_power_label)

# Create a button widget
button = tk.Button(master=root, text="Grab Screenshot", command=export_ui)
button.place(x=1, y=120)

label_work = tk.Label(root, text="0 work")
label_work.place(x=300, y=30)
# Create a Label widget for the text
label = tk.Label(root, text="Use slider to adjust size of displayed data")
label.place(x=600, y=30)
# create a slider widget to adjust the point size
slider = tk.Scale(master=root, from_=1, to=60, orient=tk.HORIZONTAL)
slider.set(60) # set initial value
slider.place(x=650, y=50)

# Start the update loop
update_data()

# Run the Tkinter event loop
tk.mainloop()
