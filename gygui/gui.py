import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QFileDialog, QMessageBox, QColorDialog, QFormLayout,
                             QFrame)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from pyvistaqt import QtInteractor

class GyroidGeneratorGUI(QMainWindow):
    def __init__(self, gyroid_generator, visualization):
        super().__init__()
        self.gyroid_generator = gyroid_generator
        self.visualization = visualization
        self.setWindowTitle("Radially Symmetrical Gyroid Generator")
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowIcon(QIcon('icon.png'))  # Add an icon file to your project
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Setup the left panel for parameters and buttons
        self.setup_left_panel(main_layout)

        # Right panel for visualization
        self.plotter = QtInteractor(self)
        main_layout.addWidget(self.plotter, 2)

        self.gyroid_mesh = None
        self.gyroid_colors = [[1, 1, 1], [0, 0, 0]]  # Default colors: white and black

    def setup_left_panel(self, main_layout):
        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.StyledPanel)
        left_panel.setFrameShadow(QFrame.Raised)
        left_layout = QVBoxLayout(left_panel)
        main_layout.addWidget(left_panel, 1)
        
        # Parameter inputs and buttons
        form_layout = QFormLayout()
        self.params = self.create_param_inputs(form_layout)
        left_layout.addLayout(form_layout)
        self.create_buttons(left_layout)

    def create_param_inputs(self, layout):
        default_params = {'res': 80, 'a': 24, 'b': 24, 'c': 10, 'r1': 12, 'r2': 0,
                          'phi_scale': 8, 'cell_radius': 2, 'cell_height': 3}
        param_descriptions = {
            'res': 'Resolution of the grid in each dimension. Higher values create more detailed structures but increase computation time.',
            'a': 'Dimension length along the X-axis. Affects the overall width of the gyroid.',
            'b': 'Dimension length along the Y-axis. Affects the overall depth of the gyroid.',
            'c': 'Dimension length along the Z-axis. Affects the overall height of the gyroid.',
            'r1': 'Inner radius of the gyroid structure. Determines the size of the central void.',
            'r2': 'Outer radius of the gyroid structure. Determines the overall thickness of the structure.',
            'phi_scale': 'Scaling factor for the angular coordinate. Affects the number of twists in the structure.',
            'cell_radius': 'Radius of the cells in the gyroid structure. Affects the size of individual "pores" in the structure.',
            'cell_height': 'Height of the cells in the gyroid structure. Affects the vertical spacing of features.'
        }
        param_labels = {
            'res': 'Resolution',
            'a': 'X-axis Length',
            'b': 'Y-axis Length',
            'c': 'Z-axis Length',
            'r1': 'Inner Radius',
            'r2': 'Outer Radius',
            'phi_scale': 'Angular Scaling Factor',
            'cell_radius': 'Cell Radius',
            'cell_height': 'Cell Height'
        }
        params = {}
        for key, value in default_params.items():
            label, line_edit = self.create_param_input(key, value, param_labels[key], param_descriptions[key])
            layout.addRow(label, line_edit)
            params[key] = line_edit
        return params

    def create_param_input(self, key, default_value, label_text, description):
        label = QLabel(f"{label_text}:")
        label.setFont(QFont("Arial", 10))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        line_edit = QLineEdit(str(default_value))
        line_edit.setToolTip(description)
        line_edit.setFixedWidth(100)
        line_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #555;
                border-radius: 4px;
                padding: 2px;
            }
        """)
        
        return label, line_edit

    def create_buttons(self, layout):
        button_layout = QHBoxLayout()
        
        generate_button = QPushButton("Generate Gyroid")
        generate_button.clicked.connect(self.generate_gyroid)
        generate_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button_layout.addWidget(generate_button)

        save_button = QPushButton("Save STL/OBJ")
        save_button.clicked.connect(self.save_mesh)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #007B9A;
            }
        """)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)

    def generate_gyroid(self):
        try:
            params = {k: float(v.text()) for k, v in self.params.items()}
            params['res'] = int(params['res'])
            self.gyroid_mesh = self.gyroid_generator.generate(params)

            # Visualize
            self.visualization.render(self.plotter, self.gyroid_mesh, self.gyroid_colors)

            QMessageBox.information(self, "Success", "Gyroid generated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate gyroid: {str(e)}")

    def save_mesh(self):
        if self.gyroid_mesh is None:
            QMessageBox.warning(self, "Warning", "Please generate a gyroid first.")
            return

        options = "STL Files (*.stl);;OBJ Files (*.obj)"
        filename, filetype = QFileDialog.getSaveFileName(self, "Save STL/OBJ", "", options)

        if filename:
            try:
                if filetype == "OBJ Files (*.obj)":
                    self.gyroid_generator.save_obj(self.gyroid_mesh, filename)
                else:
                    self.gyroid_generator.save_stl(self.gyroid_mesh, filename)
                QMessageBox.information(self, "Success", f"Mesh saved as {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save mesh: {str(e)}")

    def choose_color(self, color_index):
        color = QColorDialog.getColor()
        if color.isValid():
            self.gyroid_colors[color_index - 1] = [color.red() / 255, color.green() / 255, color.blue() / 255]
            if self.gyroid_mesh:
                self.visualization.render(self.plotter, self.gyroid_mesh, self.gyroid_colors)