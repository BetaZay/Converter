# Media Converter

The Media Converter application is a graphical user interface (GUI) tool that allows users to convert images and videos to different formats. It supports drag-and-drop functionality and provides a progress bar and status messages during the conversion process. The application is built using Python with the Tkinter library for the GUI, and it uses ttkbootstrap for styling, Pillow for image processing, and moviepy for video processing.

## Features

- **Drag-and-Drop Interface**: Easily add files for conversion by dragging and dropping them into the application window.
- **Format Conversion**:
  - Images: Convert between various image formats including PNG, JPG, JPEG, BMP, and GIF.
  - Videos: Convert between various video formats including MP4, AVI, MOV, WMV, and FLV.
- **Progress Indication**: Visual progress bars and status messages indicating the conversion progress.
- **Speed Selection**: Choose the conversion speed (Slow, Normal, Fast), which adjusts the number of processing threads.
- **Output Directory Selection**: Easily select the output directory for converted files.

## Installation

To install the required dependencies, create a virtual environment and use the requirements.txt file:


```
python -m venv env
source env/bin/activate  # On Windows use env\Scripts\activate
pip install -r requirements.txt
```

## Usage

To run the Media Converter application:

```
python main.py
```

1. Drag and drop image or video files into the application window.
2. Select the desired output format from the dropdown menu.
3. Choose the conversion speed (Slow, Normal, Fast).
4. Click the "Convert" button to start the conversion process.
5. Monitor the progress using the progress bars and status messages.
6. Access the converted files in the selected output directory.

## Supported Formats

### Image Formats
- PNG
- JPG/JPEG
- BMP
- GIF

### Video Formats
- MP4
- AVI
- MOV
- WMV
- FLV

## Dependencies

- Python 3.6+
- Tkinter
- ttkbootstrap
- Pillow
- moviepy

## Contributing

Contributions to improve the Media Converter application are welcome. Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.