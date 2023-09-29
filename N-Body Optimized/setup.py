
import numpy as np
import math
#Create a data type for quadrants

#constraints:
#points must be between 0 and x in both x and y directions for this case.

#quadrant structure

def getRadius(x1,y1, x2,y2):
    return math.sqrt(((y2-y1))**2 + ((x2)-(x1))**2)

class Quadrant:
    def __init__(self, size, origin):
        self.size = size #int,float,or double
        self.origin = origin # coordinates    
    def contains(self,sample_x,sample_y):
        if (self.origin[0] < sample_x and sample_x < self.origin[0]+self.size and self.origin[1]< sample_y and sample_y < self.origin[1]+self.size):
            return True
        else: return False 

    def northWest(self):
        return Quadrant(size = self.size/2, origin = (self.origin[0]+self.size/2, self.origin[1]))
    
    def northEast(self):
        return Quadrant(size = self.size/2, origin = (self.origin[0]+self.size/2, self.origin[1]+self.size/2))

    def southWest(self):
        return Quadrant(size = self.size/2, origin = self.origin)
    
    def southEast(self):
        return Quadrant(size = self.size/2, origin = (self.origin[0], self.origin[1]+self.size/2))

#body structure

class body:
    def __init__(self, mass, initialPositionX, initialPositionY):
        self.mass = mass
        self.pX = initialPositionX
        self.pY = initialPositionY
        self.netforceX = 0
        self.netforceY = 0
        self.velocity = [0,0] #planets start with no inital velocity (duh)

    def isEqual(self, otherBody): #check to make sure body isnt itself in tree traversal, defined as two bodies with same mass at same point.
        if isinstance(otherBody,body):
            return (self.mass == otherBody.mass and otherBody.pX and otherBody.pY)
        else: return False
    
    def forceReset(self):
        self.netforceX = 0
        self.netforceY = 0

    def isin(self, target_quadrant):
        if target_quadrant.contains(self.pX,self.pY):
            return True
        else: return False

    def updatePosition(self, dt): #update position assuming force changed 
        accelerationX = (self.netforceX/self.mass)
        accelerationY = (self.netforceY/self.mass)

        newVelocityX = self.velocity[0] + accelerationX*dt
        newVelocityY = self.velocity[1] + accelerationY*dt

        self.velocity[0] = (newVelocityX)
        self.velocity[1] = (newVelocityY)

        newPositionX = self.pX + newVelocityX*dt
        newPositionY = self.pY + newVelocityY*dt

        self.pX = newPositionX
        self.pY = newPositionY

#tree structure
        
class BHtree:
    def __init__(self, quadr):
        self.theta = 0.5
        self.body = None
        self.quad = quadr
        self.NW = None
        self.NE = None
        self.SW = None
        self.SE = None

    def createChildren(self):
        self.NW = BHtree(self.quad.northWest())
        self.NE = BHtree(self.quad.northEast())
        self.SW = BHtree(self.quad.southWest())
        self.SE = BHtree(self.quad.southEast())

    def isEmpty(self):
        if (self.body == None and self.NW == None and self.NE == None and self.SW == None and self.SE == None):
            return True
        else: return False
    
    def isLeaf(self):
        if (self.body != None and self.NW == None and self.NE == None and self.SW == None and self.SE == None):
            return True
        else: return False

    def isinternal(self):
        if ((not self.isLeaf) and (not self.isEmpty)):
            return True
        else: return False

    def adjustCOM(self,bodyA,bodyB):
        self.body = body(mass = bodyA.mass+bodyB.mass, initialPositionX = (bodyA.pX*bodyA.mass + bodyB.pX*bodyB.mass) / (bodyA.mass+bodyB.mass), initialPositionY = (bodyA.pY*bodyA.mass + bodyB.pY*bodyB.mass) / (bodyA.mass+bodyB.mass))

    def updateForce(self, body):

        if (self.isinternal() and ((self.size/getRadius(body.pX, body.pY, self.body.pX, self.body.pY)) < self.theta)): # base case 1: are we far enough away to just treat the bodies as a COM? If yes, compute the force and update passed in body's force. this can only happen if we are at an internal node.
            G = 6.67*(10**-11)
            radius = getRadius(body.pX, self.body.pX, body.pY, self.body.pY)
            force = (G)*((self.body.mass*body.mass)/radius)
            forceX = force*((self.body.pX - body.pX))
            forceY = force*((self.body.pY- body.pY))
            body.netforceX += forceX
            body.netforceY += forceY

        elif (self.isLeaf() and (not self.body.isEqual(body))): #base case 2: are we at a singular body node?
            G = 6.67*(10**-11)
            radius = getRadius(body.pX, body.pY, self.body.pX, self.body.pY)
            force = (G)*((self.body.mass*body.mass)/radius)
            forceX = force*((self.body.pX - body.pX))
            forceY = force*((self.body.pY- body.pY))
            body.netforceX += forceX
            body.netforceY += forceY

        else: #recurse through each child, this MUST be an internal node in which we are too close to approximate the internal node as one body
            for child in [self.NE, self.NW, self.SE, self.SW]:
                if child != None:
                    child.updateForce(body)
#addNode

def addNode(tree, body):
    if tree.isEmpty(): #base case 1, found an empty spot to put a body (tree object with no body mass and no children)
        tree.body = body

    elif tree.isinternal(): #in the case of internal (sum of children) node, add body to this nodes COM, and see if theres a spot to put him as a child, if not, then it just keeps recursing till it does
        tree.adjustCOM(tree.body,body)
        if body.isin(tree.NW.quad):
            addNode(tree.NW,body)
        elif body.isin(tree.NE.quad):
            addNode(tree.NE,body)
        elif body.isin(tree.SW.quad):
            addNode(tree.SW,body)
        else:
            addNode(tree.SE,body)

    else: #external node, tree object has a body but no children (collision), so we have to make children and reinsert the bodies. This may have to happen again and again (more recursion)

        tree.createChildren()
        
        if body.isin(tree.NW.quad):
            addNode(tree.NW,body)
        elif body.isin(tree.NE.quad):
            addNode(tree.NE,body)
        elif body.isin(tree.SW.quad):
            addNode(tree.SW,body)
        else:
            addNode(tree.SE,body)

        if tree.body.isin(tree.NW.quad):
            addNode(tree.NW,tree.body)
        elif tree.body.isin(tree.NE.quad):
            addNode(tree.NE,tree.body)
        elif tree.body.isin(tree.SW.quad):
            addNode(tree.SW,tree.body)
        else:
            addNode(tree.SE,tree.body)

        tree.adjustCOM(tree.body,body)

        
        

