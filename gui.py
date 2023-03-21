import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.image as mpimg
import csv
from PIL import Image, ImageTk


# Define the update interval in seconds
UPDATE_INTERVAL = 1

# Create the Tkinter GUI window
root = tk.Tk()
root.title("Sensor Data Graph")
root.geometry("1000x1000")
root.configure(bg='#FFFFFF')

# Create canvas to make distinct cololors
canvas_side = tk.Canvas(master=root, width=100, height=1000, bg='#365274', borderwidth=0, highlightthickness=0)
canvas_top = tk.Canvas(master=root, width=1000, height=100, bg='#18315A', borderwidth=0, highlightthickness=0)
canvas_side.place(x=0,y=0)
canvas_top.place(x=0,y=0)

# Add logo
# Load the image file using Pillow
pil_image = Image.open("1483-0.png")
resize = pil_image.resize([95,95])

# Convert the PIL Image object to a Tkinter PhotoImage object
tk_image = ImageTk.PhotoImage(resize)

# Add the image to the canvas at position (0, 0)
canvas_logo = tk.Canvas(master=root, width=95, height=95)
canvas_logo.create_image(0, 0, anchor=tk.NW, image=tk_image)
canvas_logo.place(x=0,y=0)

# Create a Matplotlib figure and plot the initial data
fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)
line, = ax.plot([], [])
ax.set_xlabel('Time (s)')
ax.set_ylabel('Sensor Reading')
ax.set_title('Sensor Data')

# Create a canvas to display the Matplotlib figure
canvas_fig1 = FigureCanvasTkAgg(fig, master=root)
canvas_fig1.draw()
canvas_fig1.get_tk_widget().place(x=120, y=120)

# Read data from CSV file
def read_data():
    with open('sensor_data.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    x_values = [float(row[0]) for row in data]
    y_values = [float(row[1]) for row in data]
    size = int(slider.get())
    line.set_xdata(x_values)
    line.set_ydata(y_values)
    
    # set the limits of the x-axis
    print('size: ',size)
    x_min = (100-size)
    print('x_min', x_min)
    x_max = 100
    print('x_max',x_max)
    ax.set_xlim(x_min, x_max)
    
    y_min = min(y_values)
    y_max = max(y_values)
    ax.set_ylim(y_min, y_max)

    ax.autoscale_view(True,True,True)
    canvas_fig1.draw()

# Update the data at the specified interval
def update_data():
    read_data()
    root.after(UPDATE_INTERVAL * 100, update_data)

# Create a button to manually update the data
#def update_button():
    #read_data()

# Create a button widget
#button = tk.Button(master=root, text="Update Data", command=update_button)
#button.place(x=15, y=120)

# create a slider widget to adjust the point size
slider = tk.Scale(master=root, from_=1, to=100, orient=tk.HORIZONTAL)
slider.set(100) # set initial value
slider.place(x=700, y=200)

# Start the update loop
update_data()

# Run the Tkinter event loop
tk.mainloop()
