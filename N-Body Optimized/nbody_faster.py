from nbhclasses import *
from nbhclasses import body
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random

def nbody_faster(quadSize, quadStart, numberOfBodies, timestep, time):

    #plotting 
    
    fig, ax = plt.subplots()

    # Initialize an empty scatter plot
    sc = ax.scatter([], [], marker='o', label='Planet Position')

    # Set axis limits (adjust as needed)
    ax.set_xlim(0, quadSize)
    ax.set_ylim(0, quadSize)

    #sim variables

    initial_quadrant = Quadrant(quadSize, quadStart)

    bodyList = [] #list we will use to keep track of body (planet) objects

    for i in range(numberOfBodies): 

        #generate random params per body given constraints
        mass = random.randint(1,10000)
        positionX = random.uniform(initial_quadrant.origin[0], initial_quadrant.size)
        positionY = random.uniform(initial_quadrant.origin[1], initial_quadrant.size)

        bodyList.append(body(mass = mass, initialPositionX = positionX, initialPositionY = positionY))

    bodyList.append(body(mass = 1000000, initialPositionX = 500, initialPositionY = 500))
    endtime = time
    
    for step in range(0, endtime, timestep): #begin simulation
        #new tree instance at beginning of every loop
        looped_tree = BHtree(initial_quadrant) 
        for Body in bodyList: #NlogN
            #then, recursively insert body into tree using add node.
            addNode(looped_tree, Body)
    
        for Body in bodyList: #NlogN
            Body.forceReset()
            looped_tree.updateForce(Body)
            Body.updatePosition(timestep)
        
        print("new X body position for the same body: ", bodyList[1].pX)

        # Update the plot
        sc.set_offsets([(Body.pX, Body.pY) for Body in bodyList])
        # Pause to display the frameB
        plt.pause(.01)
        # Redraw the plot
        plt.draw()


if __name__ == "__main__":
    quadSize = int(input("Size of simulation Area: "))
    numberOfBodies = int(input("Number of planets you would like to simulate: "))
    endtime = int(input("How long would you like to make the simulation: "))
    timestep = int(input("Timestep for simulation: "))

    nbody_faster(quadSize,(0,0),numberOfBodies, timestep, endtime)

    





