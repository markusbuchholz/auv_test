import numpy as np
import matplotlib.pyplot as plt


'''
One common approach is to use a potential field around the obstacle.
When the vehicle gets close to the obstacle, it will experience a repulsive force that pushes it away.
This force can be combined with the LOS guidance to ensure the vehicle avoids the obstacle.

'''



# Define the desired path using waypoints
waypoints = np.array([[0, 0], [10, 10], [20, 0], [30, 10]])

# Parameters
L = 5.0  # Look-ahead distance
dt = 0.1  # Time step
T = 30.0  # Total simulation time
v = 2.0  # Constant speed of the ASV
k = 0.1  # Control gain

# Obstacle parameters
obstacle_center = np.array([10, 5])
obstacle_radius = 3.0
K_rep = 5.0  # Repulsion coefficient

# Initial conditions
x, y, psi = 0, 0, np.pi/4  # Starting at the first waypoint with a 45-degree heading

# Lists to store trajectory for plotting
x_traj, y_traj = [x], [y]

for t in np.arange(0, T, dt):
    # Find the current segment of the path
    for i in range(len(waypoints) - 1):
        A, B = waypoints[i], waypoints[i+1]
        AB = B - A
        AP = np.array([x, y]) - A
        proj_len = np.dot(AP, AB) / np.linalg.norm(AB)
        if 0 <= proj_len <= np.linalg.norm(AB):
            break

    # Find the look-ahead point
    along_path = proj_len + L
    if along_path > np.linalg.norm(AB):
        along_path = np.linalg.norm(AB)
    LA = A + (along_path / np.linalg.norm(AB)) * AB

    # Compute the LOS angle
    delta = np.arctan2(LA[1] - y, LA[0] - x) - psi

    # Check proximity to the obstacle and compute repulsion angle
    dist_to_obstacle = np.linalg.norm(np.array([x, y]) - obstacle_center) - obstacle_radius
    if dist_to_obstacle < L:
        repulsion_angle = np.arctan2(y - obstacle_center[1], x - obstacle_center[0])
        delta += K_rep * (1/dist_to_obstacle - 1/L) * (repulsion_angle - psi)

    # Update the vehicle's heading based on the LOS angle and repulsion angle
    psi += k * delta * dt

    # Update the vehicle's position
    x += v * np.cos(psi) * dt
    y += v * np.sin(psi) * dt

    # Store the trajectory for plotting
    x_traj.append(x)
    y_traj.append(y)

# Plotting
plt.figure()
plt.plot(waypoints[:, 0], waypoints[:, 1], 'g-', label='Desired Path')
plt.plot(x_traj, y_traj, 'b-', label='ASV Trajectory')
plt.scatter(waypoints[:, 0], waypoints[:, 1], c='red', marker='o', label='Waypoints')
plt.gca().add_patch(plt.Circle(obstacle_center, obstacle_radius, color='r', label='Obstacle'))
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.title('LOS Guidance with Obstacle Avoidance')
plt.grid(True)
plt.show()
