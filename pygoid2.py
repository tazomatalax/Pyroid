import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage.measure import marching_cubes


def gyroid(x, y, z, scale=1):
    return np.sin(x/scale)*np.cos(y/scale) + np.sin(y/scale)*np.cos(z/scale) + np.sin(z/scale)*np.cos(x/scale)

def create_radial_gyroid(radius, height, wall_thickness, cell_radius, cell_height, arc_count, approx_thickness):
    resolution = 100
    theta = np.linspace(0, 2*np.pi, resolution)
    z = np.linspace(0, height, resolution)
    r = np.linspace(radius - wall_thickness, radius, resolution)

    theta, z, r = np.meshgrid(theta, z, r)
    
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    scale = cell_radius / np.pi
    
    gyroid_values = gyroid(x/scale, y/scale, z/(cell_height/2/np.pi), scale)
    
    # Create a radial pattern
    angle_step = 2 * np.pi / arc_count
    for i in range(arc_count):
        angle = i * angle_step
        rot_x = x * np.cos(angle) - y * np.sin(angle)
        rot_y = x * np.sin(angle) + y * np.cos(angle)
        gyroid_values += gyroid(rot_x/scale, rot_y/scale, z/(cell_height/2/np.pi), scale)

    gyroid_values /= arc_count  # Normalize

    vertices, faces, _, _ = marching_cubes(gyroid_values, level=0)
    
    # Scale vertices back to original dimensions
    vertices[:, 0] = vertices[:, 0] * (radius * 2) / resolution - radius
    vertices[:, 1] = vertices[:, 1] * (radius * 2) / resolution - radius
    vertices[:, 2] = vertices[:, 2] * height / resolution

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    
    return mesh

# Parameters from the image
radius = 12
height = 50
wall_thickness = 10
cell_radius = 6
cell_height = 6
arc_count = 6
approx_thickness = 0.5

# Create the gyroid
gyroid_mesh = create_radial_gyroid(radius, height, wall_thickness, cell_radius, cell_height, arc_count, approx_thickness)

# Save the mesh as an STL file
gyroid_mesh.export('radial_gyroid.stl')

# Render the gyroid
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(gyroid_mesh.vertices[:, 0], gyroid_mesh.vertices[:, 1], gyroid_mesh.vertices[:, 2],
                triangles=gyroid_mesh.faces, cmap=plt.cm.viridis)
plt.show()