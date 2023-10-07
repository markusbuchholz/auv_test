import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def voronoi_3d(grid_size, points):
    """Generate a 3D Voronoi diagram for a given set of points."""
    image = np.zeros((grid_size, grid_size, grid_size, 4), dtype=np.float32)  
    
    for z in range(grid_size):
        for y in range(grid_size):
            for x in range(grid_size):
                min_dist = float('inf')
                j = -1
                for i, (px, py, pz) in enumerate(points):
                    dist = (px - x) ** 2 + (py - y) ** 2 + (pz - z) ** 2
                    if dist < min_dist:
                        min_dist = dist
                        j = i
                image[z, y, x] = (j * 50 % 256 / 255, j * 100 % 256 / 255, j * 150 % 256 / 255, 0.2)  

    return image

def plot_voronoi_3d(image, points):
    """Plot the 3D Voronoi diagram."""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    z, y, x = np.where(np.any(image[..., :3] > 0, axis=-1))
    colors = image[z, y, x]
    ax.scatter(x, y, z, c=colors)

   
    px, py, pz = zip(*points)
    ax.scatter(px, py, pz, c='red', s=100, marker='o', label='Seed Points')
    ax.legend()
    plt.title(" Voronoid 3D diagram constructed from information from sonar")

    plt.show()


points = [(5, 5, 5), (15, 15, 15), (25, 5, 5), (10, 25, 25)]
image = voronoi_3d(30, points)
plot_voronoi_3d(image, points)
