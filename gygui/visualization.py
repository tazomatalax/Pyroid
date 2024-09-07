import numpy as np

class GyroidVisualization:
    def render(self, plotter, gyroid_mesh, gyroid_colors):
        plotter.clear()
        
        # Calculate normalized radial distance and blend colors
        r_values = np.sqrt(gyroid_mesh.points[:, 0]**2 + gyroid_mesh.points[:, 1]**2 + gyroid_mesh.points[:, 2]**2)
        r_normalized = np.clip(r_values / np.max(r_values), 0, 1)
        blended_colors = np.outer(1 - r_normalized, gyroid_colors[0]) + np.outer(r_normalized, gyroid_colors[1])

        plotter.add_mesh(gyroid_mesh, scalars=blended_colors, rgb=True, show_scalar_bar=False)
        plotter.add_bounding_box()
        plotter.show_axes()
        plotter.reset_camera()
