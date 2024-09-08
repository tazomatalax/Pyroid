# Radially Symmetrical Gyroid Generator

## 🚧 Work in Progress 🚧

This project is currently under active development. Features and functionality may change, and there might be bugs or incomplete aspects.


## Description

The Radially Symmetrical Gyroid Generator is a Python-based application that allows users to create and visualize customizable gyroid structures. It provides a graphical user interface for adjusting various parameters to generate unique, radially symmetrical gyroid models.
<img width="731" alt="image" src="https://github.com/user-attachments/assets/741ab68a-3688-4f59-9f43-9f8c42e98ab8">

## Current Features

- Interactive GUI for parameter input
- Real-time 3D visualization of the generated gyroid
- Customizable gyroid properties (dimensions, cell sizes, wall thickness, etc.)
- Dual-color visualization with adjustable intersect angle
- STL/OBJ export functionality for 3D printing

## Installation

### Prerequisites

- Python 3.7+
- PyQt5
- PyVista
- NumPy
- trimesh

### Steps

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/gyroid-generator.git
   ```
2. Navigate to the project directory:
   ```
   cd gyroid-generator
   ```
3. Create Virtual Environment (optional but reccomended)
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt # or pip install numpy pyvista trimesh PyQt5 pyvistaqt
   ```

## Usage

Run the application by executing:

```
python gyroid.py
```

Use the GUI to adjust parameters and generate your custom gyroid structure. Click "Generate Gyroid" to create the model and "Save STL" to export it for 3D printing.

## Known Issues

- Performance may degrade with very high resolution settings
- Some parameter combinations may produce unexpected results

## Planned Features

- [ ] Improved error handling and user feedback
- [ ] Additional gyroid types and variations
- [ ] Performance optimizations for handling higher resolutions
- [ ] More export options (e.g., OBJ, STEP formats)
- [ ] Undo/Redo functionality
- [ ] Importing .STL or other bodies to use as an implicit body to apply gyroid latticing

## Contributing

As this project is still in development, contributions are welcome! Please feel free to submit issues or pull requests.

## License

[MIT License](LICENSE)

## Disclaimer

This software is provided "as is", without warranty of any kind. Use at your own risk.
