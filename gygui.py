import sys
import pyvista as pv
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from pyvistaqt import QtInteractor

class GyroidGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Radially Symmetrical Gyroid Generator")
        self.setGeometry(100, 100, 1000, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Left panel for parameters
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        main_layout.addWidget(left_panel, 1)

        # Parameter inputs
        self.params = {}
        default_params = {
            'res': 100, 'a': 24, 'b': 24, 'c': 50, 'r1': 12, 'r2': 2,
            'phi_scale': 6, 'wall_thickness': 10, 'cell_radius': 6, 'cell_height': 6
        }
        for key, value in default_params.items():
            layout = QHBoxLayout()
            layout.addWidget(QLabel(f"{key}:"))
            self.params[key] = QLineEdit(str(value))
            layout.addWidget(self.params[key])
            left_layout.addLayout(layout)

        # Buttons
        generate_button = QPushButton("Generate Gyroid")
        generate_button.clicked.connect(self.generate_gyroid)
        left_layout.addWidget(generate_button)

        save_button = QPushButton("Save STL")
        save_button.clicked.connect(self.save_stl)
        left_layout.addWidget(save_button)

        # Right panel for visualization
        self.plotter = QtInteractor(self)
        main_layout.addWidget(self.plotter, 2)

        self.gyroid_mesh = None

    def generate_gyroid(self):
        try:
            params = {k: float(v.text()) for k, v in self.params.items()}
            params['res'] = int(params['res'])

            # Generate gyroid
            kx, ky, kz = [2*np.pi/params[p] for p in ('a', 'b', 'c')]
            r_aux, phi, z = np.mgrid[0:params['a']:params['res']*1j, 0:params['b']:params['res']*1j, 0:params['c']:params['res']*1j]

            r = (params['r2'] - params['r1'])/params['a'] * r_aux + params['r1']

            def Gyroid(x, y, z):
                scale_x = 2 * np.pi * params['cell_radius'] / params['a']
                scale_y = 2 * np.pi * params['cell_radius'] / params['b']
                scale_z = 2 * np.pi * params['cell_height'] / params['c']
                return np.cos(x*scale_x)*np.sin(y*scale_y) + np.cos(y*scale_y)*np.sin(z*scale_z) + np.cos(z*scale_z)*np.sin(x*scale_x)

            fun_values = Gyroid(r_aux, phi * params['phi_scale'], z)

            mask = (r >= (params['r1'] - params['wall_thickness'])) & (r <= params['r1'])
            fun_values[~mask] = 1

            x = r * np.cos(phi*ky)
            y = r * np.sin(phi*ky)
            grid = pv.StructuredGrid(x, y, z)
            grid["vol"] = fun_values.ravel('F')
            self.gyroid_mesh = grid.contour([0])

            # Visualize
            self.plotter.clear()
            self.plotter.add_mesh(self.gyroid_mesh, scalars=self.gyroid_mesh.points[:, -1], show_scalar_bar=False)
            self.plotter.add_bounding_box()
            self.plotter.show_axes()
            self.plotter.reset_camera()

            QMessageBox.information(self, "Success", "Gyroid generated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate gyroid: {str(e)}")

    def save_stl(self):
        if self.gyroid_mesh is None:
            QMessageBox.warning(self, "Warning", "Please generate a gyroid first.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Save STL", "", "STL Files (*.stl)")
        if filename:
            self.gyroid_mesh.save(filename)
            QMessageBox.information(self, "Success", f"STL file saved as {filename}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GyroidGeneratorGUI()
    window.show()
    sys.exit(app.exec_())