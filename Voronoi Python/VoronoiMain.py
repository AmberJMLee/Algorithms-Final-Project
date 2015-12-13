__author__ = 'Amy Shi, Amber Lee, Fred Ayi-Quaye'

from tkinter import *
import random
import math
from math import sqrt
from PIL import Image
from voronoiCell import *
from matplotlib.tri import Triangulation
import numpy as np
np.set_printoptions(threshold=np.nan)
 #This will contain all of the lines that were generated from the Green and Gibson algorithm
#voronoiCells = []
animate = False
#scale = 3
#seed = 7
def voronoi(triangles):
    return 0;
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
    #voronoiLines = []
    #voronoiLines.append(Line(start, end))

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
    #voronoiLines.append(Line(start, end))
    return Line(Point(start.x, start.y), Point(end.x, end.y))

def intersects(pt1, pt2, pt3, pt4): # Always check the third element!
    line1= []
    line2 = []
    line1.append([pt1[0], pt1[1]])
    line1.append([pt2[0], pt2[1]])
    line2.append([pt3[0], pt3[1]])
    line2.append([pt1[0], pt1[1]])
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return[0, 0, False]

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return [x, y, True]

def circumcenter(A, B, C):
    a = B[0] - A[0]
    b = B[1] - A[1]
    c = C[0] - A[0]
    d = C[1] - A[1]
    e = a* (A[0] + B[0]) + b * (A[1] + B[1])
    f = c *(A[0] + C[0]) + d * (A[1] + C[1])
    g = 2 * (a * (C[1] - B[1]) - b * (C[0] - B[0]))
    if(abs(g) < 0.000001):
        minx = min(A[0], B[0], C[0])
        miny = min(A[1], B[1], C[1])
        dx = (max(A[0], B[0], C[0]) - minx) * 0.5
        dy = (max(A[1], B[1], C[1]) - miny) * 0.5
        xvalue = minx + dx
        yvalue = miny + dy
        radius = sqrt(dx * dx + dy * dy)
        return [xvalue, yvalue, radius]
    else:
        xvalue = (d*e - b*f) / g
        yvalue = (a*f - c*e) / g
        dx = xvalue - A[0]
        dy = yvalue - A[1]
        radius = sqrt(dx * dx + dy * dy)
        return [xvalue, yvalue, radius]

def create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

def distance(pt1, pt2):
    return math.hypot(pt2.x-pt1.x, pt2.y-pt1.y)

class Window():
    def __init__(self):
        #Let's create a text button
        #self.T = Text(root, height=2, width=50)
        #self.T.pack()
        Label(text="Welcome to the Voronoi Painter.").pack(side=TOP)

        #Let's create a textbox
        #Label(text='Please enter an image file to use and press button.').pack(side=TOP,padx=10,pady=10)
        def onok():
            imageName = self.entry.get()
            seed = self.seed.get()
            scale = self.scale.get()
            #caller(imageName, seed, scale)
            reload(self, imageName, int(seed), int(scale))
            if animate == True:
                self.w.after(100, onok)
        def animateit():
            global animate
            animate = True
            onok()
        def halt():
            global animate
            animate = False
        #def caller(imageName, seed, scale):
        #    try:
        #        reload(self, imageName, seed, scale)
        #        self.w.after(50, caller(imageName, seed, scale))
        #    except (AttributeError, IOError, FileNotFoundError):
        #        print("No")
        #This represents the left column.
        self.group = LabelFrame()
        self.group.pack(side=LEFT)
        Label(self.group, text='Project created by Amber Lee, Amy Shi, and Fred Ayi-Quaye').pack()
        Label(self.group).pack()
        Label(self.group, text='Image File').pack()
        self.entry = Entry(self.group, width=50)
        self.entry.insert(0, 'kitten.png')
        self.entry.pack()
        Label(self.group, text='Data point scale').pack()
        self.seed = Entry(self.group, width=25)
        self.seed.insert(0, '7')
        self.seed.pack()
        Label(self.group, text='Image scale').pack()
        self.scale = Entry(self.group, width=25)
        self.scale.insert(0, '3')
        self.scale.pack()
        Button(self.group, text='Generate Voronoi Painting', command=onok).pack()
        Button(root, text='Exit', command=window_close).pack(side=BOTTOM)
        Button(self.group, text='Animate it!', command=animateit).pack()
        Button(self.group, text='Stop animation...', command=halt).pack()
        self.w = Canvas(root, width=1000, height=1000, bg='black')
        self.w.pack(side=RIGHT)

def reload(self, imageName, seed, scale):
    try:
        #Let's create a canvas

        #voronoiCircles = []
        self.w.pack()
        self.w.delete("all")
        #Let's create an image
        image = Image.open(imageName)
        colors = []
        pixels = image.load()
        width, height = image.size
        #print(width)
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
                #colors.append(cpixel)
                #print(cpixel)
                foo = random.randint(1, seed)
                #if (round(sum(cpixel)) / float(len(cpixel)) > 127) & (x%foo == 0) & (y%foo == 0):
                if ( x%foo == 0) and (y%foo == 0):
                    all_pixels.append(255)
                    points.append(Point(x*scale, y*scale))
                    xarray.append(x*scale)
                    yarray.append(y*scale)
                    colors.append(cpixel)
                    #self.w.create_oval(x*2, y*2, x*2+1, y*2+1, fill="black")
                #else:
                 #   all_pixels.append(0)                #print(all_pixels)

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
            #print(circumcircle(circle))
            #red= colors[triangle[0]][0]
            try:
                red=colors[triangle[0]][0]
                green= colors[triangle[0]][1]
                blue= colors[triangle[0]][2]
                mycolor = '#%02x%02x%02x' % (red, green, blue)
            except IndexError:
                if colors[triangle[0]][1] > 100:
                    mycolor='black'
                else:
                    mycolor='white'
            self.w.create_polygon([x1, y1], [x2, y2], [x3, y3], fill=mycolor)
            center = circumcenter([x1, y1], [x2, y2], [x3, y3])
            bisector1 = [[(x1+x2)/2], [(y1+y2)/2]]
            bisector2 = [[(x2+x3)/2], [(y2+y3)/2]]
            bisector3 = [[(x3+x1)/2], [(y3+y1)/2]]
            self.w.create_line(center[0], center[1], bisector1[0], bisector1[1])
            self.w.create_line(center[0], center[1], bisector2[0], bisector2[1])
            self.w.create_line(center[0], center[1], bisector3[0], bisector3[1])
            #self.w.create_oval(center[0]-1, center[1]-1, center[0]+1, center[1]+1, fill="black")
            #create_circle(self.w, center[0], center[1], center[2])
            #voronoiCircles.append(center)
    except (AttributeError, IOError, FileNotFoundError):
        pass
        """
        if len(voronoiCells) == 0:
            voronoiCells.append(Cell([x1, y1], [[x2, y2], [x3, y3]]))
            voronoiCells.append(Cell([x2, y2], [[x1, y1], [x3, y3]]))
            voronoiCells.append(Cell([x3, y3], [[x1, y1], [x2, y2]]))
        for voronoiCell in voronoiCells:
            if voronoiCell.shares(x1, y1):
                voronoiCell.adjacent.append([x2, y2])
                voronoiCell.adjacent.append([x3, y3])
            if voronoiCell.shares(x2, y2):
                voronoiCell.adjacent.append([x1, y1])
                voronoiCell.adjacent.append([x3, y3])
            if voronoiCell.shares(x3, y3):
                voronoiCell.adjacent.append([x1, y1])
                voronoiCell.adjacent.append([x2, y2])
            else:
                voronoiCells.append(Cell([x1, y1], [[x2, y2], [x3, y3]]))
                voronoiCells.append(Cell([x2, y2], [[x1, y1], [x3, y3]]))
                voronoiCells.append(Cell([x3, y3], [[x1, y1], [x2, y2]]))
            #print("Hello")
    print(points)
    for voronoiCell in voronoiCells:
        points = []
        for adjacent in voronoiCell.adjacent:
            points.append(intersects(drawPerpendicular([voronoiCell.center[0], voronoiCell.center[1]]), drawPerpendicular(adjacent[0], adjacent[1])))
        self.w.create_polygon(self, [points[0][0], points[0][1]], [points[1][0], points[1][1]], [points[2][0], points[2][1]], fill="black")
        #print(points)
        #print("Hello")
    """


def window_close():
    root.destroy()

root = Tk()
Window()
root.title("Voronoi Painting")
root.geometry("1000x600")
root.mainloop()
