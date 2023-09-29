#imports

import numpy as np
import math
import random
import matplotlib.pyplot as plt

from numpy import linspace
import scipy
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy import signal

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

#Create a data type for quadrants

#constraints:
#points must be between 0 and 100 in both x and y directions for this case.
#points must also be bewteen 0 and 

#initialize size of largest quadrant
sizeConstraint = 100 #constrained to 100m.
startPoint = (0,0) #bottom left corner!

#min and max coords of where bodies can be from an overall standpoint
bodyCoordMin = 0 
bodyCoordMax = 100

def getRadius(x1,y1, x2,y2):
    return math.sqrt(((y2-y1))**2+((x2)-(x1)))


class Quadrant:
    def __init__(self, size, origin):
        self.size = size
        self.origin = origin        
    def contains(self,sample_x,sample_y):
        if (self.origin[0] < sample_x and sample_x < self.origin[0]+self.size and self.origin[1]< sample_y and sample_y < self.origin[1]+self.size):
            return True
        else: return False 

    def northWest(self):
        return Quadrant(self, size = self.size/2, origin = (self.origin[0]+self.size/2, self.origin[1]))
    
    def northEast(self):
        return Quadrant(self, size = self.size/2, origin = (self.origin[0]+self.size/2, self.origin[1]+self.size/2))

    def southWest(self):
        return Quadrant(self, size = self.size/2, origin = self.origin)
    
    def southEast(self):
        return Quadrant(self, size = self.size/2, origin = (self.origin[0], self.origin[1]+self.size/2))

class body:
    def __init__(self, mass, initialPositionX, initialPositionY):
        self.mass = mass
        self.pX = initialPositionX
        self.pY = initialPositionY
        self.netforceX = 0
        self.netforceY = 0
        self.velocity = (0,0) #planets start with no inital velocity (duh)

    def isin(self, quadrant):
        if quadrant.contains(self.pX,self.pY):
            return True
        else: return False
    
    def newBody(self,body_a,body_b): #return new body that combines bodies a and b
        return body(self, body_a.mass+body_b.mass, x = (body_a.pX*body_a.mass + body_b.pX*body_b.mass) / (body_a.mass+body_b.mass), y = (body_a.pY*body_a.mass + body_b.pY*body_b.mass) / (body_a.mass+body_b.mass))
        
class BHtree:
    def __init__(self, quadrant):
        self.body = None
        self.quad = quadrant
        self.NW = None
        self.NE = None
        self.SW = None
        self.SE = None

    def isNew(self):
        if (self.body == None and self.NW == None and self.NE == None and self.SW == None and self.SE == None):
            return True
        else: return False
    
    def isExternal(self):
        if (self.body != None and self.NW == None and self.NE == None and self.SW == None and self.SE == None):
            return True
        else: return False

    def isInternal(self):
        if (self.body != None and (self.NW != None or self.NE != None or self.SW != None or self.SE != None)):
            return True
        else: return False
        
    def insertBody(self, body):
        if self.body == None:
            self.body = body
        else: self.body = self.body.newbody(self.body,body) #if its an external node, add the body to the 

    def updateForce(self, body):
        sumOfForcesX = 0  
        sumOfForcesY = 0
        radius = getRadius(body.pX, self.body.pX, body.pY, self.body.pY)
        force = (6.67*(10**-11))*((self.body.mass*body.mass)/radius)
        forceX = force*((self.body.pX - body.pX))
        forceY = force*((self.body.pY- body.pY))
        sumOfForcesX += forceX
        sumOfForcesY += forceY
        body.netforceX = sumOfForcesX
        body.netforceY = sumOfForcesY


