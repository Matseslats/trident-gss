# Multithread processing of serial data
from queue import Queue
from threading import Thread
from matplotlib import projections
import serial as ps
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.cbook as cbook
import os

# Serial setup
ser = ps.Serial('COM5', 9600)

# Watermark image
imgpath = "C:\\Users\\matsh\\Documents\\cansat\\software\\gss\\trident-gss\\image-builder-python\\logo-small.png" # os.getcwd() + "\\logo-small.png"
with cbook.get_sample_data(imgpath) as file:
    im = mpimg.imread(file)

plt.ioff() # Interactive mode
plt.style.use('dark_background')

width = 50
height = 38
syncChar = [0,255,0,255]

plotPoints = 101 # -100 to 0
data = {
    "temps": [10.0] * plotPoints,
    "pressures": [100.0] * plotPoints,
    "latitudes": [69.0] * plotPoints,
    "longitudes": [16.0] * plotPoints,
    "altitudes": [0.0] * plotPoints
}
xValues = np.linspace(1-plotPoints, 0, plotPoints)
fig = plt.figure(figsize=plt.figaspect(9/16))
fig.suptitle('Trident CanSat 2022' ,fontsize = 40)

tempplot = fig.add_subplot(2,2,1)
presplot = fig.add_subplot(2,2,3)
posplot = fig.add_subplot(2,2,2, projection='3d')
picplot = fig.add_subplot(2,2,4)
fig.canvas.manager.full_screen_toggle()
fig.canvas.toolbar_visible = False
# fig.canvas.header_visible = False
# fig.canvas.footer_visible = False
fig.figimage(im, 10, 10, zorder=3, alpha=1) # Watermark

# Setup graphs
templine, = tempplot.plot(xValues, data["temps"], linewidth=2.0, color = "blue") 
tempplot.set_title('Temperature')
presline, = presplot.plot(xValues, data["pressures"], linewidth=2.0, color = "green")
presplot.set_title('Pressure')
posline, = posplot.plot3D(data["latitudes"], data["longitudes"], data["altitudes"], 'orange')    
posplot.set_title('Location')
picplot.set_title("Live feed")

print("Setup complete")


def create_blank(width, height):
    # Create new image(numpy array) filled with certain color in RGB
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed((0,0,255)))
    # Fill image with color
    image[:] = color

    return image

img0 = create_blank(width,height)
# pic = Image.new(mode="RGB", size=(width, height))

# Plot the data
def plot(a):
    while True:
        global fig, templine, tempplot, presline, presplot, picplot, img0, data
        # print("Updating graph")
        templine.set_ydata(data["temps"])
        tempplot.set(ylim=(0, 20), yticks=np.arange(0, 25), xlim=(1-plotPoints, 0), xticks=np.arange((1-plotPoints), 0, 10)) # xlim=(1-plotPoints, 0), xticks=np.arange((1-plotPoints), 0, 10), 
        presline.set_ydata(data["pressures"])
        presplot.set(ylim=(97, 103), yticks=np.arange(97, 103),xlim=(1-plotPoints, 0), xticks=np.arange((1-plotPoints), 0, 10))

        # Plot 3d position
        global posline
        posline.remove()
        posline, = posplot.plot3D(data["latitudes"], data["longitudes"], data["altitudes"], 'orange')    

        picplot = plt.imshow(img0)
        # print("Graph data updated")
        time.sleep(1/30)
    

    # print("Redrawing")
    # # plt.draw()
    # print("Flushing")
    # # fig.canvas.flush_events()
    # print("Redrew")

x = y = 0
lastpx1 = lastpx2 = 0

# Modify next pixel of image
def setNextPixel(value):
  global x, y, width, height, img0
  if x == width-1:
    if y == height-1:
      # Exclude special start/stop char
      y = 0
      x = -4
      # Save img
      cv2.imwrite("out.png", img0)
    else:
      y += 1
      x = 0
  else:
    x += 1
  
#   print("x:", x,", y:",y," value: ", value)
  img0[y,x] = value
#   if x < 0:
#     1 == 1 # Sync

# Processing of data
last_processed_FC = -200
duplicates = 0
def process_data(p):
    global img0, x, y, lastpx1, lastpx2
    global last_processed_FC, duplicates
    # Check if frame is valid

    # Extract values
    FC = int(p[0:4], 16) # To Int (bytes, base 16)
    # Check if frame has been processed last time, if so register it as a duplicate
    if FC != last_processed_FC: # New frame detected
        # Inform about how many times last frame was read
        # print(last_processed_FC, ":")
        # print("  Duplicates: ", duplicates)
        duplicates = 0
        # Get the other values
        # How many frames were dropped?
        if last_processed_FC == -200: # First frame, dont correct for this
            dropped = 0
        else:
            dropped = FC - last_processed_FC - 1 # DIfference = 1 means 0 dropped frames
        if dropped != 0:
            print("WARNING: %d frames dropped" % dropped)
            print("Skipped from ", last_processed_FC, " to ", FC)
            for i in range(0,dropped):
                # Compensate graphs for framedrops by adding blank values
                data["temps"].pop(0)
                data["temps"].append(None)
                data["pressures"].pop(0)
                data["pressures"].append(None)

                for j in range(0,2):
                    # Compensate with black pixels for framedrop
                    setNextPixel(0)
        
        # Process data
        TEMP = int(p[4:6], 16)
        PRES = int(p[6:8], 16)
        LAT = int(p[8:10], 16)
        LON = int(p[10:12], 16)
        ALT = int(p[12:14], 16)
        px1 = int(p[14:16], 16)
        px2 = int(p[16:18], 16)

        data["temps"].pop(0)
        data["temps"].append(TEMP)

        data["pressures"].pop(0)
        data["pressures"].append(PRES)

        data["latitudes"].pop(0)
        data["latitudes"].append(LAT)
        data["longitudes"].pop(0)
        data["longitudes"].append(LON)
        data["altitudes"].pop(0)
        data["altitudes"].append(ALT)

        # print("FC: %d, (last px 1: %d, 2: %d), px1: %d, px2: %d" % (FC, lastpx1, lastpx2, px1, px2))
        # If sync word found, start at top left
        if [lastpx1, lastpx2, px1, px2] == syncChar:
            print("SYNC")
            x = -3
            y = 0
        lastpx1 = px1
        lastpx2 = px2
        setNextPixel(px1)
        setNextPixel(px2)

    else:
        duplicates += 1

    # Save this as processed
    last_processed_FC = FC

lastpacket = b''
def split_packets(d):
    global lastpacket
    first = True # First red string should append to the start  
    # Data from serial
    buffer = d
    # print(buffer)
    # Split into packets
    # print("Packets:")
    packets = buffer.split(b'FC03')
    # print("Package amount: %d" % len(packets))
    for p in packets:
        # print("[P] Lst packet: %r" % lastpacket)
        # print("[P] Raw packet: %r" % p)
        if len(p) < 20: # Some of the package missing?
            if first:
                p = (lastpacket[len(p)-18:]) + p # Append to start
                p = p[-20:]
                # print("Add %r to the start" % lastpacket[len(p)-18:])
                first = False
        # print("[P] Packet:     %r" % p)
        if len(p) == 18:
            # try:
            process_data(p)
            # except:
            #     global stop_threads
            #     stop_threads = True
        lastpacket = p
    
    # print()
    # print("--------")
    # print()


# A thread that produces data
def producer(out_q):
    while True:
        # Read data
        buffer = ser.read(100)
        out_q.put(buffer)
        global stop_threads
        if stop_threads == True:
            exit(1)


import keyboard
import time
a = 0
stop_threads = False
def killswitch(in_q):
    global a
    while True:
        if a > 10:
            global stop_threads
            # stop_threads = True
            # time.sleep(1)
            # exit(1)

# A thread that consumes data
def consumer(in_q):
    global a
    while True:
        # Get some data
        data = in_q.get()
        # Process the data
        split_packets(data)
        a += 1
        if stop_threads == True:
            exit(1) # Works, but is not a good solution

if __name__ == '__main__':     
    # Create the shared queue and launch both threads
    q = Queue()
    dataprocesser = Thread(target = consumer, args =(q, ))
    datagatherer = Thread(target = producer, args =(q, ))
    killer = Thread(target = killswitch, args =(q, ))
    grapher = Thread(target= plot, args=(q,))
    dataprocesser.start()
    datagatherer.start()
    # killer.start()

    grapher.start()
    fig.show()
    while True:
        time.sleep(1/30)
        fig.canvas.draw()
        fig.canvas.flush_events()
# while True:
# plot()
# time.sleep(2)
# plt.show()
