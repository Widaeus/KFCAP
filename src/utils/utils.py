import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
from src.models.session_manager import session_manager
from src.models.project import redcapProj
from src.utils.reader_prep import import_data
import re

entry_data_path = None

import urllib.request

def validate_api_token(api_token, label_validation):
    if len(api_token) < 32:
        label_validation.configure(text="Invalid token", text_color="red")
    else:
        try:
            project = redcapProj(api_url='https://redcap.ki.se/api/', api_token=api_token)
            project_info = project.export_project_info()
            project_title = project_info.get('project_title', 'Unknown Project')
            label_validation.configure(text=f"Valid token: {project_title}", text_color="green")
            return True
        except Exception as e:
            label_validation.configure(text="Invalid token", text_color="red")
            return False

def browse_files(entry_widget):
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry_widget.delete(0, ctk.END)
    entry_widget.insert(0, filename)

def run_process(entry_data_path, combo_data_form):
    # Get the inputs from the GUI
    data_path = entry_data_path.get()
    data_form = combo_data_form.get()  

    if not data_path or not data_form:
        messagebox.showerror("Error", "All fields must be filled in.")
        return

    cached_api_token = session_manager.get_api_token()

    try:
        if cached_api_token:
            project_instance = session_manager.get_project_instance()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to REDCap: {e}")
        return

    # Process the data
    try:
        if data_form == "OLO data":
            # Convert and clean data
            second_column = import_data(data_path, project_instance)
            messagebox.showinfo("Success", f"The following IDs were successfully imported: {', '.join(second_column)}")
        else:
            raise ValueError(f"Data form {data_form} is not supported as of this moment.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during data processing: {e}")

def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    win.geometry(f"{width}x{height}+{x}+{y}")

def load_csv(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df

def find_study_id(project):
    project_info = project.export_project_info()
    custom_record_label = project_info.get('custom_record_label', '')

    match = re.search(r'\[(.*?)\]', custom_record_label)
    if match:
        study_id = match.group(1)
        # Sanitize study_id by removing illegal characters
        study_id = re.sub(r'[^\w\-]', '', study_id)
        return study_id
    return None