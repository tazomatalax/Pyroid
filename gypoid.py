import pyvista as pv
import numpy as np
import os

def get_user_input(prompt, default, type_cast=float):
    user_input = input(f"{prompt} (default: {default}): ")
    return type_cast(user_input) if user_input else default

def generate_gyroid(params):
    # Derived parameters
    kx, ky, kz = [2*np.pi/lattice_param for lattice_param in (params['a'], params['b'], params['c'])]
    r_aux, phi, z = np.mgrid[0:params['a']:params['res'], 0:params['b']:params['res'], 0:params['c']:params['res']]

    # Convert r_aux range to actual radii
    r = (params['r2'] - params['r1'])/params['a'] * r_aux + params['r1']

    def Gyroid(x, y, z):
        scale_x = 2 * np.pi * params['cell_radius'] / params['a']
        scale_y = 2 * np.pi * params['cell_radius'] / params['b']
        scale_z = 2 * np.pi * params['cell_height'] / params['c']
        return np.cos(x*scale_x)*np.sin(y*scale_y) + np.cos(y*scale_y)*np.sin(z*scale_z) + np.cos(z*scale_z)*np.sin(x*scale_x)

    # Compute data for cylindrical gyroid
    fun_values = Gyroid(r_aux, phi * params['phi_scale'], z)

    # Apply wall thickness
    mask = (r >= (params['r1'] - params['wall_thickness'])) & (r <= params['r1'])
    fun_values[~mask] = 1  # Set values outside the wall to 1 (which will be removed in the contour)

    # Compute Cartesian coordinates for grid points
    x = r * np.cos(phi*ky)
    y = r * np.sin(phi*ky)
    grid = pv.StructuredGrid(x, y, z)
    grid["vol"] = fun_values.ravel('F')
    contours = grid.contour([0])

    return contours

def save_stl(mesh, filename):
    mesh.save(filename)
    print(f"STL file '{filename}' has been generated.")

def visualize_gyroid(contours):
    pv.set_plot_theme('document')
    plotter = pv.Plotter()
    plotter.add_mesh(contours, scalars=contours.points[:, -1], show_scalar_bar=False)
    plotter.add_bounding_box()
    plotter.show_axes()
    plotter.enable_terrain_style()
    plotter.show()

# Default parameters
default_params = {
    'res': 100j,
    'a': 24,
    'b': 24,
    'c': 50,
    'r1': 12,
    'r2': 2,
    'phi_scale': 6,
    'wall_thickness': 10,
    'cell_radius': 6,
    'cell_height': 6
}

# Main program
if __name__ == "__main__":
    print("Welcome to the Radially Symmetrical Gyroid Generator!")
    print("You can press Enter to use the default value for each parameter.")

    # Get user input for parameters
    params = {}
    for key, value in default_params.items():
        params[key] = get_user_input(f"Enter value for {key}", value, type(value))

    # Generate the gyroid
    print("Generating gyroid...")
    gyroid_mesh = generate_gyroid(params)
    print("Gyroid generated successfully!")

    while True:
        action = input("Do you want to (s)ave STL, (v)isualize, or (q)uit? ").lower()
        
        if action == 's':
            filename = input("Enter filename for STL (default: radial_gyroid.stl): ") or "radial_gyroid.stl"
            save_stl(gyroid_mesh, filename)
        elif action == 'v':
            print("Launching 3D visualization...")
            visualize_gyroid(gyroid_mesh)
        elif action == 'q':
            print("Thank you for using the Radially Symmetrical Gyroid Generator!")
            break
        else:
            print("Invalid input. Please try again.")