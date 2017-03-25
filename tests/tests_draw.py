from module import vtx_draw
from module import vtx_com
from Tkinter import *

root = Tk()
draw = Canvas(root, width=500, height=50, bg="black")
draw.pack()

for i in range(500):
  fillS = vtx_draw.getStrengthColour(((i-250.0)/50), 1)
  print fillS
  draw.create_rectangle(i, 0, i, 50, fill=fillS, width=0)

while True:
  root.update()
  root.update_idletasks()
