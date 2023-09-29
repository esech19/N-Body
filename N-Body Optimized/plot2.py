from nbhclasses import *
from nbhclasses import body
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random

def nbody_faster(quadSize, quadStart, numberOfBodies, timestep, time):
    # Plotting
    fig, ax = plt.subplots()

    # Initialize an empty scatter plot
    sc = ax.scatter([], [], marker='o', label='Planet Position')

    # Set axis limits (adjust as needed)
    ax.set_xlim(0, quadSize)
    ax.set_ylim(0, quadSize)

    def update(frame):
        nonlocal bodyList
        ax.clear()

        for Body in bodyList:
            Body.forceReset()
            looped_tree.updateForce(Body)
            Body.updatePosition(timestep)

        sc = ax.scatter([Body.pX for Body in bodyList], [Body.pY for Body in bodyList], marker='o', label='Planet Position')
        return sc,

    initial_quadrant = Quadrant(quadSize, quadStart)

    bodyList = []

    for i in range(numberOfBodies):
        mass = random.randint(1, 1000)
        positionX = random.uniform(initial_quadrant.origin[0], initial_quadrant.size)
        positionY = random.uniform(initial_quadrant.origin[1], initial_quadrant.size)

        bodyList.append(body(mass=mass, initialPositionX=positionX, initialPositionY=positionY))

    endtime = time

    looped_tree = BHtree(initial_quadrant)

    ani = FuncAnimation(fig, update, frames=range(0, endtime, timestep), blit=True, repeat=False)

    plt.show()

if __name__ == "__main__":
    quadSize = int(input("Size of simulation Area: "))
    numberOfBodies = int(input("Number of planets you would like to simulate: "))
    endtime = int(input("How long would you like to make the simulation: "))
    timestep = int(input("Timestep for simulation: "))

    nbody_faster(quadSize, (0, 0), numberOfBodies, timestep, endtime)