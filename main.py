import os
import tempfile
import tkinter as tk
import threading
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, messagebox
from PIL import Image
from moviepy.editor import VideoFileClip
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import subprocess
from proglog import ProgressBarLogger
import sys

# Ensure tkdnd library is found
os.environ['TKDND_LIBRARY'] = os.path.join(os.path.dirname(__file__), 'tkdnd', 'library')

# List to store the paths of dropped files
dropped_files = []

class TkProgressLogger(ProgressBarLogger):
    def __init__(self, progress_bar, task_output_var, total_files, file_type):
        super().__init__()
        self.progress_bar = progress_bar
        self.task_output_var = task_output_var
        self.total_files = total_files
        self.current_file_index = 0
        self.file_type = file_type

    def callback(self, **changes):
        for (key, value) in changes.items():
            if key == 'bars':
                bar_name = list(value.keys())[0]
                bar_data = value[bar_name]
                progress = bar_data['index'] / bar_data['total']
                percentage = progress * 100
                self.progress_bar['value'] = percentage
                self.task_output_var.set(f"Converting {self.current_file_index + 1}/{self.total_files} {self.file_type.upper()}... ({percentage:.2f}%)")
                root.update_idletasks()

    def bars_callback(self, bar, attr, value, old_value=None):
        percentage = (value / self.bars[bar]['total']) * 100
        self.progress_bar['value'] = percentage
        self.task_output_var.set(f"Converting {self.current_file_index + 1}/{self.total_files} {self.file_type.upper()}... ({percentage:.2f}%)")
        root.update_idletasks()

def convert_image(image_paths, output_format, output_dir):
    try:
        total_files = len(image_paths)
        for index, image_path in enumerate(image_paths):
            img = Image.open(image_path)
            file_name, _ = os.path.splitext(os.path.basename(image_path))
            new_file_path = os.path.join(output_dir, f"{file_name}.{output_format}")
            img.save(new_file_path)
            progress['value'] = (index + 1) / total_files * 100
            task_output.set(f"Converting {index + 1}/{total_files} {output_format.upper()}... ({(index + 1) / total_files * 100:.2f}%)")
        messagebox.showinfo("Success", "Images converted successfully!")
        progress['value'] = 0
        task_output.set("")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")
        progress['value'] = 0
        task_output.set("")

def convert_video(video_paths, output_format, output_dir, threads):
    try:
        total_files = len(video_paths)
        temp_dir = tempfile.gettempdir()
        codec = {
            "mp4": "libx264",
            "avi": "rawvideo",
            "mov": "libx264",
            "wmv": "libx264",
            "flv": "flv"
        }.get(output_format, "libx264")
        
        for index, video_path in enumerate(video_paths):
            tk_progress_logger = TkProgressLogger(progress_video, task_output_video, total_files, output_format)
            tk_progress_logger.current_file_index = index
            clip = VideoFileClip(video_path)
            file_name, _ = os.path.splitext(os.path.basename(video_path))
            new_file_path = os.path.join(output_dir, f"{file_name}.{output_format}")
            temp_audiofile = os.path.join(temp_dir, f"{file_name}_temp_audio.mp3")
            clip.write_videofile(new_file_path, codec=codec, logger=tk_progress_logger, temp_audiofile=temp_audiofile, remove_temp=True, threads=threads)
            progress_video['value'] = (index + 1) / total_files * 100
            task_output_video.set(f"Converting {index + 1}/{total_files} {output_format.upper()}... ({(index + 1) / total_files * 100:.2f}%)")
        messagebox.showinfo("Success", "Videos converted successfully!")
        progress_video['value'] = 0
        task_output_video.set("")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")
        progress_video['value'] = 0
        task_output_video.set("")

def drop(event):
    files = root.tk.splitlist(event.data)
    for file in files:
        if os.path.isfile(file):
            dropped_files.append(file)
            if notebook.index(notebook.select()) == 0:
                file_listbox.insert(tk.END, file)
            else:
                file_listbox_video.insert(tk.END, file)

def browse_files(file_types, listbox):
    files = filedialog.askopenfilenames(filetypes=file_types)
    for file in files:
        if file:
            dropped_files.append(file)
            listbox.insert(tk.END, file)

def select_output_dir():
    dir_name = filedialog.askdirectory()
    if dir_name:
        output_dir.set(dir_name)

def open_output_dir():
    if os.path.isdir(output_dir.get()):
        if os.name == 'nt':  # For Windows
            os.startfile(output_dir.get())
        elif os.name == 'posix':  # For MacOS and Linux
            subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', output_dir.get()])
    else:
        messagebox.showerror("Error", "Output directory does not exist.")

def convert_images():
    output_format = image_format.get()
    if not dropped_files:
        messagebox.showwarning("No files", "No files to convert.")
        return
    if not output_dir.get():
        messagebox.showwarning("No output directory", "Please select an output directory.")
        return
    threading.Thread(target=convert_image, args=(dropped_files, output_format, output_dir.get())).start()

def convert_videos():
    output_format = video_format.get()
    speed = conversion_speed.get()
    threads = {"Slow": 1, "Normal": 2, "Fast": 4}[speed]
    if not dropped_files:
        messagebox.showwarning("No files", "No files to convert.")
        return
    if not output_dir.get():
        messagebox.showwarning("No output directory", "Please select an output directory.")
        return
    threading.Thread(target=convert_video, args=(dropped_files, output_format, output_dir.get(), threads)).start()

def on_tab_change(event):
    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")
    if tab_text == "Images":
        default_pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
        output_dir.set(default_pictures_dir)
    else:
        default_videos_dir = os.path.join(os.path.expanduser("~"), "Videos")
        output_dir.set(default_videos_dir)

def open_combobox(event):
    event.widget.event_generate('<Down>')

# Initialize the main window
root = TkinterDnD.Tk()
root.title("Media Converter")
root.minsize(600, 400)

# Set the application icon
datafile = "app-icon.ico"
if not hasattr(sys, "frozen"):
    datafile = os.path.join(os.path.dirname(__file__), datafile)
else:
    datafile = os.path.join(sys.prefix, datafile)

root.iconbitmap(default=datafile)

# Apply the bootstrap theme
style = tb.Style(theme="darkly")

# Create a notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
notebook.bind("<<NotebookTabChanged>>", on_tab_change)

# Create frames for each tab
image_frame = ttk.Frame(notebook)
video_frame = ttk.Frame(notebook)

notebook.add(image_frame, text="Images")
notebook.add(video_frame, text="Videos")

# Setup the image tab
image_frame.columnconfigure([0, 1, 2, 3], weight=1)
image_frame.rowconfigure([0, 1, 2, 3, 4, 5], weight=1)

# Create a frame for drag-and-drop area in the image tab
drop_frame_image = ttk.Frame(image_frame, width=200, height=150, bootstyle="secondary")
drop_frame_image.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
drop_frame_image.drop_target_register(DND_FILES)
drop_frame_image.dnd_bind('<<Drop>>', drop)

# Create a label for instructions inside the drag-and-drop frame
drop_label_image = ttk.Label(drop_frame_image, text="Drop Images Here", bootstyle="light")
drop_label_image.place(relx=0.5, rely=0.5, anchor="center")

# Listbox to show the list of image files
file_listbox = tk.Listbox(image_frame, bg='#404040', fg='#ffffff', selectbackground='#606060', selectforeground='#ffffff')
file_listbox.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

# Dropdown for selecting the output file format for images
image_format = tk.StringVar(value="png")
format_menu_image = ttk.Combobox(image_frame, textvariable=image_format, values=["png", "jpg", "jpeg", "bmp", "gif"], width=10, bootstyle="primary", state="readonly")
format_menu_image.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
format_menu_image.bind("<Button-1>", open_combobox)

# Entry and button for output directory for images
output_dir = tk.StringVar()
output_dir_entry = ttk.Entry(image_frame, textvariable=output_dir, bootstyle="secondary")
output_dir_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")

# Button to select output directory
select_output_dir_button = ttk.Button(image_frame, text="Select Output Directory", command=select_output_dir, bootstyle="primary")
select_output_dir_button.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")

# Task output label and progress bar for images
task_output = tk.StringVar()
task_output_label = ttk.Label(image_frame, textvariable=task_output, bootstyle="light")
task_output_label.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

progress = ttk.Progressbar(image_frame, orient="horizontal", mode="determinate", maximum=100)
progress.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

# Frame for control buttons for images
control_frame_image = ttk.Frame(image_frame)
control_frame_image.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

# Button to browse image files
browse_button_image = ttk.Button(control_frame_image, text="Browse", command=lambda: browse_files([("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")], file_listbox), bootstyle="success")
browse_button_image.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Button to convert images
convert_button_image = ttk.Button(control_frame_image, text="Convert", command=convert_images, bootstyle="warning")
convert_button_image.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

# Button to open output directory
open_output_button = ttk.Button(control_frame_image, text="Open Output Directory", command=open_output_dir, bootstyle="info")
open_output_button.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

# Setup the video tab
video_frame.columnconfigure([0, 1, 2, 3], weight=1)
video_frame.rowconfigure([0, 1, 2, 3, 4, 5], weight=1)

# Create a frame for drag-and-drop area in the video tab
drop_frame_video = ttk.Frame(video_frame, width=200, height=150, bootstyle="secondary")
drop_frame_video.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
drop_frame_video.drop_target_register(DND_FILES)
drop_frame_video.dnd_bind('<<Drop>>', drop)

# Create a label for instructions inside the drag-and-drop frame
drop_label_video = ttk.Label(drop_frame_video, text="Drop Videos Here", bootstyle="light")
drop_label_video.place(relx=0.5, rely=0.5, anchor="center")

# Listbox to show the list of video files
file_listbox_video = tk.Listbox(video_frame, bg='#404040', fg='#ffffff', selectbackground='#606060', selectforeground='#ffffff')
file_listbox_video.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

# Dropdown for selecting the output file format for videos
video_format = tk.StringVar(value="mp4")
format_menu_video = ttk.Combobox(video_frame, textvariable=video_format, values=["mp4", "avi", "mov", "wmv", "flv"], width=10, bootstyle="primary", state="readonly")
format_menu_video.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
format_menu_video.bind("<Button-1>", open_combobox)

# Entry and button for output directory for videos
output_dir_video = ttk.Entry(video_frame, textvariable=output_dir, bootstyle="secondary")
output_dir_video.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")

# Button to select output directory
select_output_dir_button_video = ttk.Button(video_frame, text="Select Output Directory", command=select_output_dir, bootstyle="primary")
select_output_dir_button_video.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")

# Dropdown for selecting the conversion speed
conversion_speed = tk.StringVar(value="Normal")
speed_menu_video = ttk.Combobox(video_frame, textvariable=conversion_speed, values=["Slow", "Normal", "Fast"], width=10, bootstyle="primary", state="readonly")
speed_menu_video.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
speed_menu_video.bind("<Button-1>", open_combobox)

# Task output label and progress bar for videos
task_output_video = tk.StringVar()
task_output_label_video = ttk.Label(video_frame, textvariable=task_output_video, bootstyle="light")
task_output_label_video.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

progress_video = ttk.Progressbar(video_frame, orient="horizontal", mode="determinate", maximum=100)
progress_video.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

# Frame for control buttons for videos
control_frame_video = ttk.Frame(video_frame)
control_frame_video.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

# Button to browse video files
browse_button_video = ttk.Button(control_frame_video, text="Browse", command=lambda: browse_files([("Video files", "*.mp4;*.avi;*.mov;*.wmv;*.flv")], file_listbox_video), bootstyle="success")
browse_button_video.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Button to convert videos
convert_button_video = ttk.Button(control_frame_video, text="Convert", command=convert_videos, bootstyle="warning")
convert_button_video.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

# Button to open output directory
open_output_button_video = ttk.Button(control_frame_video, text="Open Output Directory", command=open_output_dir, bootstyle="info")
open_output_button_video.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

# Set the default output directories
default_pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
default_videos_dir = os.path.join(os.path.expanduser("~"), "Videos")

output_dir.set(default_pictures_dir)

# Run the application
root.mainloop()
