import numpy as np
import matplotlib.pyplot as plt

# Define the desired path using waypoints
waypoints = np.array([[0, 0], [10, 10], [20, 0], [30, 10]])

# Parameters
L = 5.0  # Look-ahead distance
dt = 0.1  # Time step
T = 30.0  # Total simulation time
v = 2.0  # Constant speed of the ASV
k = 0.1  # Control gain

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

    # Update the vehicle's heading based on the LOS angle
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
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.title('LOS Guidance Simulation')
plt.grid(True)
plt.show()
