# SERVER
# from logging import exception
import socket
import time
# from unicodedata import decimal
import cv2
import random

im = cv2.imread('demo-grayscale-4.png', cv2.IMREAD_GRAYSCALE) # Can be many different formats.
print(im.shape)  # Get the width and hight of the image for iterating over
width = im.shape[1]
height = im.shape[0]

x = 1
y = 37
FC = 0
frameDrop = 0 # Simulate dropped frames
temp = 10.0
pres = 100.00
lat = 69.0
long = 16.0
alt = 2.0

# print("Testing img")
# print("%d, %d (Top left): %d" % (0, 0, im[0,0]))
# print("%d, %d (Top right): %d" % (0, width-1, im[width-1,0]))
# print("%d, %d (Bottom left): %d" % (height-1,0, im[0,height-1]))
# print("%d, %d (Bottom right): %d" % (height-1, width-1, im[width-1,height-1]))
value = im[0,0]


syncChar = [0,255,0,255]

print(syncChar[-4])
print(syncChar[-3])
print(syncChar[-2])
print(syncChar[-1])

def nextPixel():
  global x, y, width, height
  if x == width-1:
    # print("A")
    if y == height-1:
      # print("B")
      # Special start/stop char
      y = 0
      x = -4
    else:
      # print("C")
      y += 1
      x = 0
  else:
    # print("D")
    x += 1
  
  # print(x,y," ")
  value = im[y,x]
  if x < 0:
    value = syncChar[x]
  # print(value)
  return value

def server():
  global FC, frameDrop, temp, pres, lat, long, alt
  host = socket.gethostname()   # get local machine name
  port = 8080  # Make sure it's within the > 1024 $$ <65535 range
  print("[INFO] Started server at:")
  print("[INFO] Name: %r:%r" % (host, port))
  s = socket.socket()
  s.bind((host, port))
  
  s.listen(1)
  client_socket, adress = s.accept()
  print("[SERVER] Connection from: " + str(adress))
  while True:
    # Simulate framedrops
    framedropcahnce = 2 #random.random()*10 # 1/x will be 'dropped'
    if framedropcahnce < 1:
      FC += 1
      nextPixel()
      nextPixel()
    else:
      pixel1 = nextPixel()
      pixel2 = nextPixel()

      temp += (random.random()-0.5)/5
      pres += (random.random()-0.5)/50
      lat += (random.random()-0.5)/5e4
      long += (random.random()-0.5)/5e4
      alt += (random.random()-0.5)/5

      data = "%d,%f,%f,%f,%f,%f,%d,%d;" % (FC, temp, pres, lat, long, alt, pixel1, pixel2)
      # print(data)
      FC += 1 + frameDrop
      # print(data)
      # print()
      client_socket.send(data.encode('utf-8'))
      time.sleep(1/14)

  client_socket.close()
  print("[INFO] Connection ended")

if __name__ == '__main__':
  #while(True):
  server()
