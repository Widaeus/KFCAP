import customtkinter as ctk
from tkinter import filedialog, messagebox
from src.redcap.project import Project
import pandas as pd
from src.utils.alert_handling import find_study_id, find_deviating_records, load_csv

entry_data_path = None

def validate_api_token(api_token, label_validation):
    if len(api_token) < 32:  # Assuming a valid API token has at least 32 characters
        label_validation.configure(text="Invalid token", text_color="red")
    else:
        try:
            project = define_url_token_project(api_token)
            project_info = project.export_project_info()
            project_title = project_info.get('project_title', 'Unknown Project')
            label_validation.configure(text=f"Valid token: {project_title}", text_color="green")
        except Exception as e:
            label_validation.configure(text="Invalid token", text_color="red")

def define_url_token_project(api_token):
    api_url = 'https://redcap.ki.se/api/'
    project = Project(api_url, api_token)
    return project

def browse_files(entry_widget):
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry_widget.delete(0, ctk.END)
    entry_widget.insert(0, filename)

def run_process(entry_data_path, entry_api_token, combo_data_form):
    # Get the inputs from the GUI
    data_path = entry_data_path.get()
    api_token = entry_api_token.get()
    data_form = combo_data_form.get()  

    if not data_path or not api_token or not data_form:
        messagebox.showerror("Error", "All fields must be filled in.")
        return

    # Define REDCap project
    try:
        project = define_url_token_project(api_token)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to REDCap: {e}")
        return

    # Process the data
    try:
        if data_form == "OLO data":
            # Convert and clean data
            second_column = import_data(data_path, project)
            messagebox.showinfo("Success", f"The following IDs were successfully imported: {', '.join(second_column)}")
        else:
            raise ValueError(f"Data form {data_form} is not supported as of this moment.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during data processing: {e}")

def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()

def display_alerts_window(records_info, root):
    study_ids = list(records_info.keys())
    current_index = [0]

    alerts_window = ctk.CTkToplevel(root)
    alerts_window.title("Deviating Records")
    center_window(alerts_window, width=600, height=850)
    
    display_frame = ctk.CTkFrame(alerts_window)
    display_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    label_study_id = ctk.CTkLabel(display_frame, text="", font=("Arial", 14, "bold"))
    label_study_id.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    ctk.CTkLabel(display_frame, text="Variable", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=5)
    ctk.CTkLabel(display_frame, text="Value", font=("Arial", 12, "bold")).grid(row=1, column=1, padx=10, pady=5)
    ctk.CTkLabel(display_frame, text="Reference", font=("Arial", 12, "bold")).grid(row=1, column=2, padx=10, pady=5)

    value_labels = []

    def update_display():
        study_id = study_ids[current_index[0]]
        total_records = len(study_ids)
        label_study_id.configure(text=f"Study ID: {study_id} ({current_index[0] + 1}/{total_records})")
        variable_info = records_info[study_id]

        for label in value_labels:
            label.destroy()
        value_labels.clear()

        row_num = 2
        for var_name, info in variable_info.items():
            var_label = ctk.CTkLabel(display_frame, text=var_name, font=("Arial", 12))
            var_label.grid(row=row_num, column=0, padx=10, pady=5)
            value_text = str(info['value']) if pd.notna(info['value']) else "N/A"
            value_label = ctk.CTkLabel(
                display_frame,
                text=value_text,
                font=("Arial", 12, "bold" if info['deviated'] else "normal"),
                text_color="red" if info['deviated'] else "black"
            )
            value_label.grid(row=row_num, column=1, padx=10, pady=5)
            ref_label = ctk.CTkLabel(display_frame, text=info['reference'], font=("Arial", 12))
            ref_label.grid(row=row_num, column=2, padx=10, pady=5)
            value_labels.extend([var_label, value_label, ref_label])
            row_num += 1

    def next_record():
        if current_index[0] < len(study_ids) - 1:
            current_index[0] += 1
            update_display()

    def previous_record():
        if current_index[0] > 0:
            current_index[0] -= 1
            update_display()

    button_frame = ctk.CTkFrame(alerts_window)
    button_frame.pack(side="bottom", pady=10)

    ctk.CTkButton(button_frame, text="Previous", command=previous_record, width=100, height=50).pack(side="left", padx=10)
    ctk.CTkButton(button_frame, text="Next", command=next_record, width=100, height=50).pack(side="right", padx=10)

    update_display()

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    win.geometry(f"{width}x{height}+{x}+{y}")
