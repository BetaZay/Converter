## Compiling the Media Converter Application

To package the Media Converter application into a standalone executable, follow these steps:

### Prerequisites
- Python 3.x
- PyInstaller

Install PyInstaller using pip:

```
pip install pyinstaller
```

### Spec File

The .spec file is used to configure the build process.

### Hook File

Create a `hook-tkinterdnd2.py` file to ensure the TkinterDnD2 package is included correctly:

"
from PyInstaller.utils.hooks import collect_data_files
datas = collect_data_files('tkinterdnd2')
"

### Compilation Command

Use the following command to compile the application into a single executable file:

"
pyinstaller main.spec
"

### Setting the Application Icon

In your `main.py` script, set the application icon as follows:

"
import sys
import os
datafile = "app-icon.ico"
if not hasattr(sys, "frozen"):
    datafile = os.path.join(os.path.dirname(__file__), datafile)
else:
    datafile = os.path.join(sys.prefix, datafile)
root.iconbitmap(default=datafile)
"

This ensures that the icon is correctly included whether the script is run directly or from a packaged executable.

### Running the Executable

After compilation, the standalone executable can be found in the `dist` directory. You can run it directly without needing to install Python or any dependencies on the target machine.