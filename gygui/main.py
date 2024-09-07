import sys
from PyQt5.QtWidgets import QApplication
from gui import GyroidGeneratorGUI
from gyroid_generator import GyroidGenerator
from visualization import GyroidVisualization

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    gyroid_generator = GyroidGenerator()
    visualization = GyroidVisualization()
    
    window = GyroidGeneratorGUI(gyroid_generator, visualization)
    window.show()
    
    sys.exit(app.exec_())
