# CLIENT
from ctypes import sizeof
import socket

from matplotlib import projections
#import keyboard      #dette har gabriel gjort
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.cbook as cbook
import os

# Watermark image
imgpath = os.getcwd() + "\\logo-small.png"
with cbook.get_sample_data(imgpath) as file:
    im = mpimg.imread(file)

plt.ion() # Interactive mode
plt.style.use('dark_background')

width = 50
height = 38
syncChar = [0,255,0,255]

plotPoints = 101 # -100 to 0
data = {
    "temps": [None] * plotPoints,
    "pressures": [None] * plotPoints,
    "latitudes": [69.0] * plotPoints,
    "longitudes": [16.0] * plotPoints,
    "altitudes": [0.0] * plotPoints
}
xValues = np.linspace(1-plotPoints, 0, plotPoints)
fig = plt.figure(figsize=plt.figaspect(2.))
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




tempcolor = "blue"

templine, = tempplot.plot(xValues, data["temps"], linewidth=2.0, color = tempcolor) 
tempplot.set_title('Temperature')
presline, = presplot.plot(xValues, data["pressures"], linewidth=2.0, color = "green")
presplot.set_title('Pressure')
posline, = posplot.plot3D(data["latitudes"], data["longitudes"], data["altitudes"], 'orange')    
posplot.set_title('Location')
picplot.set_title("Live feed")



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

x = y = 0
lastpx1 = lastpx2 = 0

def setNextPixel(value):
  global x, y, width, height
#   print(x,y," ")
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
  
  img0[y,x] = value
  if x < 0:
    1 == 1 # Sync

  # print(value)

FC = 0
lasstvalues = ""
def process(d):
    global lasstvalues
    global img0, x, y, lastpx1, lastpx2, FC
    # Check if more lines are coming, process them separately
    lines = d.split(';')
    for i in lines:
        # Splitt into seperate values
        values = i.split(',')
        if len(values) >= 1:
            if values[0] != '': # does this drop frames?
                # Check for dropped frames
                lastFC = FC
                try:
                    int(values[0])
                except:
                    break
                FC = int(values[0])
                framedrop = FC-lastFC -1
                if len(values) != 8: # Data was lost, this is a framedrop
                    framedrop = 1
                if framedrop > 0: # What happned here? Debugging ...
                    print("Verified frame:")
                    print(lasstvalues)
                    print("Frame in question:")
                    print(values)

                if framedrop != 0: # Correct for framedrops
                    print("%d frames dropped" % (framedrop))
                    for i in range(0,framedrop):
                        # Compensate graphs for framedrops
                        data["temps"].pop(0)
                        data["temps"].append(None)
                        data["pressures"].pop(0)
                        data["pressures"].append(None)
                        
                        # data["latitudes"].pop(0)
                        # data["latitudes"].append(0.0)
                        # data["longitudes"].pop(0)
                        # data["longitudes"].append(0.0)
                        # data["altitudes"].pop(0)
                        # data["altitudes"].append(0.0)

                        for j in range(0,2):
                            # Compensate with black pixels for framedrop
                            setNextPixel(0)

                if len(values) >= 3: # Enough data to process pressures
                    # Remove datapoint 0, add current value to the end
                    try:
                        data["pressures"].pop(0)
                        data["pressures"].append(float(values[2]))
                    except:
                        data["pressures"].pop(0)
                        data["pressures"].append(None)
                else: # Frame stopped, compensate
                    data["pressures"].pop(0)
                    data["pressures"].append(None)

                if len(values) >= 2: # Enough data to process temp
                    # Remove datapoint 0, add current value to the end
                    try:
                        data["temps"].pop(0)
                        data["temps"].append(float(values[1]))
                    except: 
                        data["temps"].pop(0)
                        data["temps"].append(None)
                else: # Frame stopped, compensate
                    data["temps"].pop(0)
                    data["temps"].append(None)
                
                if len(values) >= 6: # Enough data to process location
                    # Remove datapoint 0, add current value to the end
                    try:
                        data["latitudes"].pop(0)
                        data["latitudes"].append(float(values[3]))
                        data["longitudes"].pop(0)
                        data["longitudes"].append(float(values[4]))
                        data["altitudes"].pop(0)
                        data["altitudes"].append(float(values[5]))
                    except:
                        """Do nothing currently"""
                # else: # Frame stopped, compensate
                    # data["latitudes"].pop(0)
                    # data["latitudes"].append(0.0)
                    # data["longitudes"].pop(0)
                    # data["longitudes"].append(0.0)
                    # data["altitudes"].pop(0)
                    # data["altitudes"].append(0.0)

                if len(values) >= 8: # Enough data to process image?
                    try:
                        px1 = int(values[6])
                        px2 = int(values[7])
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
                    except:
                        setNextPixel(0)
                        setNextPixel(0)
                else: # Frame arrived, but cut short. Compensate with black pixels
                    setNextPixel(0)
                    setNextPixel(0)
            
                lasstvalues = values
    
    # upscale = cv2.resize(img0, None, fx=6, fy=6, interpolation=cv2.INTER_NEAREST)
    # cv2.imshow("live", upscale)
    # cv2.waitKey(1)
    # Plot data
    templine.set_ydata(data["temps"])
    tempplot.set(ylim=(0, 20), yticks=np.arange(0, 25), xlim=(1-plotPoints, 0), xticks=np.arange((1-plotPoints), 0, 10)) # xlim=(1-plotPoints, 0), xticks=np.arange((1-plotPoints), 0, 10), 
    presline.set_ydata(data["pressures"])
    presplot.set(ylim=(97, 103), yticks=np.arange(97, 103),xlim=(1-plotPoints, 0), xticks=np.arange((1-plotPoints), 0, 10))

    # Plot 3d position
    global posline
    posline.remove()
    posline, = posplot.plot3D(data["latitudes"], data["longitudes"], data["altitudes"], 'orange')    

    picplot = plt.imshow(img0)
    
    fig.canvas.draw()
    fig.canvas.flush_events()

def client():
  host = socket.gethostname()  # get local machine name
  port = 8080  # Make sure it's within the > 1024 $$ <65535 range
  
  s = socket.socket()
  s.connect((host, port))
  
  #message = input('-> ')
  while not keyboard.is_pressed("Esc"):
    data = s.recv(1024).decode('utf-8')
    process(data)
  s.close()

if __name__ == '__main__':
  client()
