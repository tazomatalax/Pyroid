import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QFileDialog, QMessageBox, QColorDialog)
from PyQt5.QtCore import Qt
from pyvistaqt import QtInteractor

class GyroidGeneratorGUI(QMainWindow):
    def __init__(self, gyroid_generator, visualization):
        super().__init__()
        self.gyroid_generator = gyroid_generator
        self.visualization = visualization
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Radially Symmetrical Gyroid Generator")
        self.setGeometry(100, 100, 1000, 600)
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
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        main_layout.addWidget(left_panel, 1)
        
        # Parameter inputs and buttons
        self.params = self.create_param_inputs(left_layout)
        self.create_buttons(left_layout)

    def create_param_inputs(self, layout):
        default_params = {'res': 100, 'a': 24, 'b': 24, 'c': 50, 'r1': 12, 'r2': 2,
                          'phi_scale': 6, 'wall_thickness': 2, 'cell_radius': 6, 'cell_height': 6}
        params = {}
        for key, value in default_params.items():
            layout.addLayout(self.create_param_input(key, value, params))
        return params

    def create_param_input(self, label_text, default_value, params):
        layout = QHBoxLayout()
        label = QLabel(f"{label_text}:")
        line_edit = QLineEdit(str(default_value))
        layout.addWidget(label)
        layout.addWidget(line_edit)
        params[label_text] = line_edit
        return layout

    def create_buttons(self, layout):
        generate_button = QPushButton("Generate Gyroid")
        generate_button.clicked.connect(self.generate_gyroid)
        layout.addWidget(generate_button)

        save_button = QPushButton("Save STL")
        save_button.clicked.connect(self.save_stl)
        layout.addWidget(save_button)

        color_button1 = QPushButton("Choose Color 1")
        color_button1.clicked.connect(lambda: self.choose_color(1))
        layout.addWidget(color_button1)

        color_button2 = QPushButton("Choose Color 2")
        color_button2.clicked.connect(lambda: self.choose_color(2))
        layout.addWidget(color_button2)

    def generate_gyroid(self):
        try:
            params = {k: float(v.text()) for k, v in self.params.items()}
            params['res'] = int(params['res'])
            self.gyroid_mesh = self.gyroid_generator.generate(params)

            # Visualize
            self.visualization.render(self.plotter, self.gyroid_mesh, self.gyroid_colors)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate gyroid: {str(e)}")

    def save_stl(self):
        if self.gyroid_mesh is None:
            QMessageBox.warning(self, "Warning", "Please generate a gyroid first.")
            return
        filename, _ = QFileDialog.getSaveFileName(self, "Save STL", "", "STL Files (*.stl)")
        if filename:
            self.gyroid_generator.save_stl(self.gyroid_mesh, filename)
            QMessageBox.information(self, "Success", f"STL file saved as {filename}")

    def choose_color(self, color_index):
        color = QColorDialog.getColor()
        if color.isValid():
            self.gyroid_colors[color_index - 1] = [color.red() / 255, color.green() / 255, color.blue() / 255]
            if self.gyroid_mesh:
                self.visualization.render(self.plotter, self.gyroid_mesh, self.gyroid_colors)
