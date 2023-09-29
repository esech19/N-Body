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

endtime = 20000 # total time of simulation
dt = 1 #timestep

G = 6.67*(10**-11)

planetList = []

def getRadius(x1,y1, x2,y2, z1, z2):
    return math.sqrt(((y2-y1))**2+((x2)-(x1))**2+((z2)-(z1))**2)

class planet:
    def __init__(self, mass, initialPositionX, initialPositionY, initialPositionZ):
        self.mass = mass
        self.netforce = []
        self.positions = [(initialPositionX, initialPositionY, initialPositionZ)]
        self.velocities = [(0,0,0)] #planets start with no inital velocity
        self.posX = []
        self.posY = []
        self.posZ = []

#create N body list
for i in range(5): #10 planets, with masses from 1-10 kg, in a space of 50 by 50 XY grid
    planetList.append(planet(random.randint(1,10000), random.randint(0,100),random.randint(0,100),random.randint(0,100)))

planetList.append(planet(40000,random.randint(0,100),random.randint(0,100),random.randint(0,100)))
    
#simulate NXN body gravitational forces and resulting velocities

for timestep in range(0, endtime, dt): #for each timestep, calculate each bodies force on each other
    for planet1 in planetList: 
        sumOfForcesX = 0  
        sumOfForcesY = 0
        sumOfForcesZ = 0
        for planet2 in planetList:
            radius = getRadius(planet1.positions[timestep][0], planet1.positions[timestep][1], planet1.positions[timestep][2], planet2.positions[timestep][0], planet2.positions[timestep][1], planet2.positions[timestep][2])
            if (radius != 0):
                force = G*(planet1.mass*planet2.mass)/radius
                forceX = force*((planet2.positions[timestep][0] - planet1.positions[timestep][0]))
                forceY = force*((planet2.positions[timestep][1]- planet1.positions[timestep][1]))
                forceZ = force*((planet2.positions[timestep][2]- planet1.positions[timestep][2]))
                sumOfForcesX += forceX
                sumOfForcesY += forceY
                sumOfForcesZ += forceZ
        planet1.netforce.append((sumOfForcesX,sumOfForcesY,sumOfForcesZ))

    for planet in planetList:
        #calculate acceleration at time t
        accelerationX = (planet.netforce[timestep][0]/planet.mass)
        accelerationY = (planet.netforce[timestep][1]/planet.mass)
        accelerationZ = (planet.netforce[timestep][2]/planet.mass)

        newVelocityX = planet.velocities[timestep][0] + accelerationX*dt
        newVelocityY = planet.velocities[timestep][1] + accelerationY*dt
        newVelocityZ = planet.velocities[timestep][2] + accelerationZ*dt

        planet.velocities.append((newVelocityX,newVelocityY,newVelocityZ))

        newPositionX = planet.positions[timestep][0] + newVelocityX*dt
        newPositionY = planet.positions[timestep][1] + newVelocityY*dt
        newPositionZ = planet.positions[timestep][2] + newVelocityZ*dt

        planet.positions.append((newPositionX,newPositionY,newPositionZ))

print(planetList[3].positions)
print(planetList[5].mass)

for planet in planetList:
    for pair in planet.positions:
        planet.posX.append(pair[0])
        planet.posY.append(pair[1])
        planet.posZ.append(pair[2])

'''
for planet in planetList:
    plt.scatter(planet.posX,planet.posY, s = planet.mass/10000)
plt.show()
'''

n_points = len(planetList[0].posX)
# Create a function to update the plot during animation
# Import necessary libraries
import numpy as np
import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# ... (previous code) ...

# Create a function to update the plot during animation
def update(frame):
    ax.cla()  # Clear the current axis
    ax.set_xlim(0, 100)  # Set X-axis limits
    ax.set_ylim(0, 100)  # Set Y-axis limits
    ax.set_zlim(0, 100)  # Set Z-axis limits
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Scatter Plot (Frame {})'.format(frame))

    for i, planet in enumerate(planetList):
        x_data = planet.posX
        y_data = planet.posY
        z_data = planet.posZ

        # Plot the planet's trajectory up to the current frame
        ax.scatter(x_data[:frame], y_data[:frame], z_data[:frame], marker='o', label=f'Planet {i + 1}')

    ax.legend()

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create an animation
ani = FuncAnimation(fig, update, frames=range(0, n_points, 100), repeat=False, interval=1)

plt.show()
    


















        