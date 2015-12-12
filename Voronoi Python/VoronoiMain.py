__author__ = 'Amy Shi, Amber Lee, Fred Ayi-Quaye'

from tkinter import *
import random
import math
import time
import doctest
from itertools import permutations
from PIL import Image
from voronoiCell import *
from matplotlib.tri import Triangulation
import numpy as np

voronoiLines = [] #This will contain all of the lines that were generated from the Green and Gibson algorithm
voronoiCells = []

#This draws a perpendicular line between all points that are closest to each other.
def nearestDistanceConnect(points, w):
    for point in points:
        closestDist = float("inf")
        closestX = 0;
        closestY = 0;
        for pointee in points: #For each point, find the point that is closest to it.
            dist = distance(point, pointee)
            if((dist < closestDist) & (dist > 0)):
                closestDist = dist
                closestX = pointee.x
                closestY = pointee.y
        print("The closest point to ", point.x, point.y, " is ", closestX, closestY)
        w.create_line(point.x, point.y, closestX, closestY, fill="#476042", width=1) #Draw a line between the closest points
        drawPerpendicular(point, Point(closestX, closestY), w) #Draw the line's perpendicular.
    return 0

#This code is most likely not going to be used, but it is a filler for now.
def drawPerpendicular(pt1, pt2, w):
    centerX = (pt1.x + pt2.x) / 2
    centerY = (pt1.y + pt2.y) / 2
    leftsize = 10
    rightsize = 10
    start = Point(0, 0)
    end = Point(0, 0)
    if pt1.y - pt2.y != 0:
        start.x = centerX - leftsize
        start.y = centerY + leftsize*((pt1.x-pt2.x)/(pt1.y-pt2.y))
        end.x = centerX + rightsize
        end.y = centerY - rightsize*((pt1.x-pt2.x)/(pt1.y-pt2.y))
        #print(centerX - 1, centerY + ((pt1.x-pt2.x)/(pt1.y-pt2.y)), " to ", centerX + 1, centerY - ((pt1.x-pt2.x)/(pt1.y-pt2.y)))
    else:
        start.x = centerX
        start.y = centerY + leftsize
        end.x = centerX
        end.y = centerY - rightsize
    w.create_line(start.x, start.y, end.x, end.y, fill="red", width=1)
    voronoiLines.append(Line(start, end))

def drawPerpendicularBisector(pt1, pt2, beginning, finish):
    centerX = (pt1.x + pt2.x) / 2
    centerY = (pt1.y + pt2.y) / 2
    start = Point(0, 0)
    end = Point(0, 0)
    if pt1.y - pt2.y != 0:
        start.x = beginning.x
        start.y = centerY + (centerX - beginning.x)*((pt1.x-pt2.x)/(pt1.y-pt2.y))
        end.x = finish.x
        end.y = centerY - (finish.x - centerX)*((pt1.x-pt2.x)/(pt1.y-pt2.y))
    else:
        start.x = centerX
        start.y = beginning.y
        end.x = centerY
        end.y = end.y
    voronoiLines.append(Line(start, end))
    return Line(Point(start.x, start.y), Point(end.x, end.y))


def distance(pt1, pt2):
    return math.hypot(pt2.x-pt1.x, pt2.y-pt1.y)

class Window():
    def __init__(self):
        #Let's create a text button
        self.T = Text(root, height=2, width=50)
        self.T.pack()
        Label(text="Welcome to the Voronoi Painter.").pack(side=TOP, padx=10, pady=10)

        #Let's create a textbox
        Label(text='Please enter an image file to use and press button.').pack(side=TOP,padx=10,pady=10)
        self.entry = Entry(root, width=50)
        self.entry.pack(side=TOP,padx=10,pady=10)
        def onok():
            imageName = self.entry.get()
            #print(imageName)
            reload(self, imageName)
            self.w.after(100, onok)
        Button(root, text='Exit', command=window_close).pack(side=BOTTOM)
        Button(root, text='Add image file', command=onok).pack(side=BOTTOM)
        self.w = Canvas(root, width=1000, height=1000)
        self.w.pack()

def reload(self, imageName):
    #Let's create a canvas
    self.w.pack()
    self.w.delete("all")
    #Let's create an image
    image = Image.open(imageName)
    pixels = image.load()
    width, height = image.size
    #Just a testing data structure. Don't use this.
    all_pixels = []
    #Use this one when doing calculations.
    points = []
    xarray = []
    yarray = []
    color = ["red", "orange", "yellow", "green", "blue", "violet"]
    #loop(self, points, pixels, all_pixels, width, height)
    for x in range(width):
        for y in range(height):
            cpixel = pixels[x, y]
            #print(cpixel)
            foo = random.randint(1, 7)
            if (round(sum(cpixel)) / float(len(cpixel)) > 127) & (x%foo == 0) & (y%foo == 0):
                all_pixels.append(255)
                points.append(Point(x*3, y*3))
                xarray.append(x*3)
                yarray.append(y*3)
                #self.w.create_oval(x*2, y*2, x*2+1, y*2+1, fill="black")
            else:
                all_pixels.append(0)
            #print(all_pixels)
    triangulation = Triangulation(xarray, yarray)
    triangles = triangulation.get_masked_triangles()
    #triangles = triangulation.triangles()
    #print(triangles)
    for triangle in triangles:
        x1 = xarray[triangle[0]]
        y1 = yarray[triangle[0]]
        x2 = xarray[triangle[1]]
        y2 = yarray[triangle[1]]
        x3 = xarray[triangle[2]]
        y3 = yarray[triangle[2]]
        circle = np.array([[x1, y1], [x2, y2], [x3, y3]])
        #print(circumcircle(circle))
        self.w.create_polygon([x1, y1], [x2, y2], [x3, y3], fill=random.choice(color))




    #plt.figure()
    #plt.gca().set_aspect('equal')
    #plt.triplot(triangulation)
    #plt.title("Triangulation")
    #plt.show()
    #nearestDistanceConnect(points, self.w)
    #for line in voronoiLines:
    #    print("(",line.start.x,",", line.start.y, ") to (", line.end.x, ",", line.end.y,")")

def intersects(l1, l2):
    l1_start = l1.start
    l1_end = l1.end
    l2_start = l2.start
    l2_end = l2.end

    l1_startx = l1_start.x
    l1_starty = l1_start.y

    l2_startx = l2_start.x
    l2_starty = l2_start.y

    l1_endx = l1_end.x
    l1_endy = l1_end.y

    l2_endx = l2_end.x
    l2_endy = l2_end.y

    m1 = (l1_starty - l1_endy) / (l1_startx - l1_endx)
    m2 = (l2_starty - l2_endy) / (l2_startx - l2_endx)

    b1 = l1_starty - m1*l1_startx
    b2 = l2_starty - m2*l2_startx

    if m1==m2 & b1 != b2:
        return False
    else:
        return True

#def circumcircle(T):
#    P1,P2,P3=T[:,0], T[:,1], T[:,2]
#    b = P2 - P1
#    c = P3 - P1
#    d=2*(b[:,0]*c[:,1]-b[:,1]*c[:,0])
#    center_x=(c[:,1]*(np.square(b[:,0])+np.square(b[:,1]))- b[:,1]*(np.square(c[:,0])+np.square(c[:,1])))/d + P1[:,0]
#    center_y=(b[:,0]*(np.square(c[:,0])+np.square(c[:,1]))- c[:,0]*(np.square(b[:,0])+np.square(b[:,1])))/d + P1[:,1]
#    return np.array((center_x, center_y)).T


def window_close():
    root.destroy()

root = Tk()
Window()
root.title("Voronoi Painting")
root.geometry("1000x600")
root.mainloop()
