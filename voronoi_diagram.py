import numpy as np
import matplotlib.pyplot as plt

def voronoi_2d(width, height, points):
    """Generate a 2D Voronoi diagram for a given set of points."""
    image = np.zeros((height, width, 4), dtype=np.float32)  
    
    for y in range(height):
        for x in range(width):
            min_dist = float('inf')
            j = -1
            for i, (px, py) in enumerate(points):
                dist = (px - x) ** 2 + (py - y) ** 2
                if dist < min_dist:
                    min_dist = dist
                    j = i
            image[y, x] = (j * 50 % 256 / 255, j * 100 % 256 / 255, j * 150 % 256 / 255, 0.2)  # Color with transparency

    return image

def plot_voronoi_2d(image, points):
    """Plot the 2D Voronoi diagram."""
    plt.imshow(image)

    # Plotting the seed points
    px, py = zip(*points)
    plt.scatter(px, py, c='red', s=100, label='Seed Points')
    plt.legend()
    plt.title(" Voronoid 2D diagram constructed from information from sonar")

    plt.show()

# Example usage:
points = [(100, 100), (300, 300), (500, 100), (200, 500)]
image = voronoi_2d(600, 600, points)
plot_voronoi_2d(image, points)
