import customtkinter as ctk
from tkinter import filedialog, messagebox
from src.redcap.project import Project
import pandas as pd
from src.utils.alert_handling import find_study_id
from src.models.session_manager import session_manager
from src.utils.reader_prep import import_data

entry_data_path = None

def validate_api_token(api_token, label_validation):
    if len(api_token) < 32:
        label_validation.configure(text="Invalid token", text_color="red")
    else:
        try:
            project = define_url_token_project(api_token)
            project_info = project.export_project_info()
            project_title = project_info.get('project_title', 'Unknown Project')
            label_validation.configure(text=f"Valid token: {project_title}", text_color="green")
            return True
        except Exception as e:
            label_validation.configure(text="Invalid token", text_color="red")
            return False

def define_url_token_project(api_token):
    api_url = 'https://redcap.ki.se/api/'
    project = Project(api_url, api_token)
    return project

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

def display_alerts_window(deviating_vars, alerts, redcap_data, project_instance, root):
    study_ids = sorted(deviating_vars.keys())
    current_index = [0]

    # Create the top-level window
    alerts_window = ctk.CTkToplevel(root)
    alerts_window.title("Deviating Records")
    center_window(alerts_window, width=600, height=850)
    
    # Display frame for alerts
    display_frame = ctk.CTkFrame(alerts_window)
    display_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Study ID Label at the top
    label_study_id = ctk.CTkLabel(display_frame, text="", font=("Arial", 14, "bold"))
    label_study_id.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    # Headers
    ctk.CTkLabel(display_frame, text="Variable", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=5)
    ctk.CTkLabel(display_frame, text="Value", font=("Arial", 12, "bold")).grid(row=1, column=1, padx=10, pady=5)
    ctk.CTkLabel(display_frame, text="Reference", font=("Arial", 12, "bold")).grid(row=1, column=2, padx=10, pady=5)

    # List to store dynamically created labels for each variable
    value_labels = []

    # Export records from project_instance
    records_df = redcap_data.set_index(find_study_id(project_instance))

    # Build a dictionary to hold the detailed info for each study_id
    records_info = {}
    for study_id in study_ids:
        # Initialize study_id entry with all alerts
        records_info[study_id] = {}
        for alert in alerts:
            for var_name, details in alert.alert_dict.items():
                value = records_df.at[study_id, var_name] if study_id in records_df.index and var_name in records_df.columns else "N/A"
                records_info[study_id][var_name] = {
                    'value': value,
                    'condition': details['reference_interval'],
                    'deviated': False
                }
        
        # Update deviating vars with actual values and deviation status
        if study_id in deviating_vars:
            for deviated_var in deviating_vars[study_id]:
                records_info[study_id][deviated_var]['deviated'] = True

    def update_display():
        """Update the display to show details for the current study ID."""
        if not study_ids:
            label_study_id.configure(text="No valid Study IDs available.")
            return

        if current_index[0] >= len(study_ids) or current_index[0] < 0:
            label_study_id.configure(text="Study ID index out of range.")
            return

        study_id = study_ids[current_index[0]]
        total_records = len(study_ids)
        label_study_id.configure(text=f"Study ID: {study_id} ({current_index[0] + 1}/{total_records})")
        variable_info = records_info[study_id]

        # Clear previous labels
        for label in value_labels:
            label.destroy()
        value_labels.clear()

        # Populate the frame with variable information
        row_num = 2
        for var_name, info in variable_info.items():
            # Variable name
            var_label = ctk.CTkLabel(display_frame, text=var_name, font=("Arial", 12))
            var_label.grid(row=row_num, column=0, padx=10, pady=5)

            # Variable value with conditional formatting for deviation
            value_text = str(info['value']) if pd.notna(info['value']) else "N/A"
            value_label = ctk.CTkLabel(
                display_frame,
                text=value_text,
                font=("Arial", 12, "bold" if info.get('deviated', False) else "normal"),
                text_color="red" if info.get('deviated', False) else "black"
            )
            value_label.grid(row=row_num, column=1, padx=10, pady=5)

            # Reference interval (the condition)
            ref_label = ctk.CTkLabel(display_frame, text=info['condition'], font=("Arial", 12))
            ref_label.grid(row=row_num, column=2, padx=10, pady=5)

            # Store the created labels
            value_labels.extend([var_label, value_label, ref_label])
            row_num += 1

    def next_record():
        """Show the next record's data if available."""
        if current_index[0] < len(study_ids) - 1:
            current_index[0] += 1
            update_display()

    def previous_record():
        """Show the previous record's data if available."""
        if current_index[0] > 0:
            current_index[0] -= 1
            update_display()

    # Button frame for navigation controls
    button_frame = ctk.CTkFrame(alerts_window)
    button_frame.pack(side="bottom", pady=10)

    ctk.CTkButton(button_frame, text="Previous", command=previous_record, width=100, height=50).pack(side="left", padx=10)
    ctk.CTkButton(button_frame, text="Next", command=next_record, width=100, height=50).pack(side="right", padx=10)

    # Initial display
    update_display()

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    win.geometry(f"{width}x{height}+{x}+{y}")
