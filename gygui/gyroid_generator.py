import numpy as np
import pyvista as pv

class GyroidGenerator:
    def generate(self, params):
        kx, ky, kz = [2*np.pi/params[p] for p in ('a', 'b', 'c')]
        r_aux, phi, z = np.mgrid[0:params['a']:params['res']*1j, 0:params['b']:params['res']*1j, 0:params['c']:params['res']*1j]
        
        r = (params['r2'] - params['r1']) / params['a'] * r_aux + params['r1']
        
        def Gyroid(x, y, z):
            scale_x = 2 * np.pi * params['cell_radius'] / params['a']
            scale_y = 2 * np.pi * params['cell_radius'] / params['b']
            scale_z = 2 * np.pi * params['cell_height'] / params['c']
            return np.cos(x * scale_x) * np.sin(y * scale_y) + np.cos(y * scale_y) * np.sin(z * scale_z) + np.cos(z * scale_z) * np.sin(x * scale_x)

        fun_values = Gyroid(r_aux, phi * params['phi_scale'], z)
        
        # Adjust wall thickness
        mask = (np.abs(fun_values) <= params['wall_thickness'])
        
        x = r * np.cos(phi * ky)
        y = r * np.sin(phi * ky)
        grid = pv.StructuredGrid(x, y, z)
        grid["mask"] = mask.ravel('F')
        
        return grid.extract_geometry()

    def save_stl(self, mesh, filename):
        mesh.save(filename)
