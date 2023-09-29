import matplotlib.pyplot as plt
import numpy as np

# Initialize figure and axis
fig, ax = plt.subplots()

# Initialize an empty scatter plot
sc = ax.scatter([], [], marker='o', label='Object Position')

# Define the time-related parameters
time = 10  # Total simulation time
dt = 1     # Time step

# Set axis limits (adjust as needed)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Create an initial set of points (modify as needed)
initial_positions = [(1, 2), (3, 4), (5, 6)]
points = initial_positions

# Create a loop to update and display the plot at each iteration
for timestep in range(0, time, dt):
    # Update point locations based on your simulation logic
    # Example: Move points randomly at each time step
    new_positions = [(x + np.random.uniform(-1, 1), y + np.random.uniform(-1, 1)) for x, y in points]
    
    # Update the scatter plot
    sc.set_offsets(new_positions)
    
    # Pause to display the frame
    plt.pause(0.01)
    
    # Redraw the plot
    plt.draw()
    
    # Assign the new positions to the points array for the next iteration
    points = new_positions

# Show the final plot
plt.show()