import customtkinter as ctk
from tkinter import filedialog, messagebox
from src.redcap.project import Project
import pandas as pd
from src.utils.alert_handling import find_study_id, find_deviating_records
from src.utils.reader_prep import import_data

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

def browse_files():
    filename = filedialog.askdirectory()
    entry_data_path.delete(0, ctk.END)
    entry_data_path.insert(0, filename)

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

def display_alerts_window(project, root):
    deviating_ids, deviations = find_deviating_records(project)
    data_redcap = project.export_records(format_type='df')
    
    study_id_column = find_study_id(project)
    
    current_index = [0]

    alerts_window = ctk.CTkToplevel(root)
    alerts_window.title("Deviating Records")
    center_window(alerts_window, width=600, height=850)
    
    display_frame = ctk.CTkFrame(alerts_window)
    display_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Display current study_id
    label_study_id = ctk.CTkLabel(display_frame, text="", font=("Arial", 14, "bold"))
    label_study_id.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    # Column headers
    ctk.CTkLabel(display_frame, text="Variable", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=5)
    ctk.CTkLabel(display_frame, text="Value", font=("Arial", 12, "bold")).grid(row=1, column=1, padx=10, pady=5)
    ctk.CTkLabel(display_frame, text="Reference", font=("Arial", 12, "bold")).grid(row=1, column=2, padx=10, pady=5)

    variable_names = [
        "bp_right_sys", "bp_left_sys", "bp_right_dia", "bp_left_dia", "pulse_right", "pulse_left",
        "wbc_109l", "plt_109l", "hgb_gl", "mcv_fl", "neut_number_109l", "lymph_number_109l",
        "mono_number_109l", "eos_number_109l", "baso_number_109l"
    ]

    plain_language_names = [
        "Systolic BP (Right)", "Systolic BP (Left)", "Diastolic BP (Right)", "Diastolic BP (Left)",
        "Pulse (Right)", "Pulse (Left)", "White Blood Cells", "Platelets", "Hemoglobin", "Mean Corpuscular Volume",
        "Neutrophils", "Lymphocytes", "Monocytes", "Eosinophils", "Basophils"
    ]
    
    reference_values = [
        "Reference: SysBP 80-180", "Reference: SysBP 80-180", "Reference: DiaBP 50-110", "Reference: DiaBP 50-110",
        "Reference: Pulse 40-120", "Reference: Pulse 40-120", "Reference: WBC 3.5-12", "Reference: Platelets 145-387",
        "Reference: Hemoglobin 117-170", "Reference: MCV 80-100", "Reference: Neutrophils 1.6-8", "Reference: Lymphocytes 1.1-3.5",
        "Reference: Monocytes 0.2-0.8", "Reference: Eosinophils 0.0-0.5", "Reference: Basophils 0.0-0.1"
    ]

    value_labels = []
    reference_labels = []

    for i, var_name in enumerate(variable_names):
        ctk.CTkLabel(display_frame, text=plain_language_names[i], font=("Arial", 12)).grid(row=i+2, column=0, padx=10, pady=5)
        value_label = ctk.CTkLabel(display_frame, text="", font=("Arial", 12))
        value_label.grid(row=i+2, column=1, padx=10, pady=5)
        value_labels.append(value_label)
        reference_label = ctk.CTkLabel(display_frame, text=reference_values[i], font=("Arial", 12))
        reference_label.grid(row=i+2, column=2, padx=10, pady=5)
        reference_labels.append(reference_label)

    # Add rows for calculated differences
    ctk.CTkLabel(display_frame, text="Systolic BP Difference", font=("Arial", 12)).grid(row=len(variable_names)+2, column=0, padx=10, pady=5)
    systolic_diff_label = ctk.CTkLabel(display_frame, text="", font=("Arial", 12))
    systolic_diff_label.grid(row=len(variable_names)+2, column=1, padx=10, pady=5)
    ctk.CTkLabel(display_frame, text="Reference: SysBP Difference <= 20", font=("Arial", 12)).grid(row=len(variable_names)+2, column=2, padx=10, pady=5)

    ctk.CTkLabel(display_frame, text="Diastolic BP Difference", font=("Arial", 12)).grid(row=len(variable_names)+3, column=0, padx=10, pady=5)
    diastolic_diff_label = ctk.CTkLabel(display_frame, text="", font=("Arial", 12))
    diastolic_diff_label.grid(row=len(variable_names)+3, column=1, padx=10, pady=5)
    ctk.CTkLabel(display_frame, text="Reference: DiaBP Difference <= 10", font=("Arial", 12)).grid(row=len(variable_names)+3, column=2, padx=10, pady=5)

    def update_display():
        study_id = deviating_ids[current_index[0]]
        total_records = len(deviating_ids)
        label_study_id.configure(text=f"Study ID: {study_id} ({current_index[0] + 1}/{total_records} records)")
        row = data_redcap[data_redcap[study_id_column] == study_id].iloc[0]
        deviation_values = deviations[study_id]
        for i, var_name in enumerate(variable_names):
            value = row[var_name] if var_name in row else ""
            if var_name in deviation_values:
                value_labels[i].configure(text=str(value), font=("Arial", 12, "bold"), fg_color="red")
            else:
                value_labels[i].configure(text=str(value), font=("Arial", 12), fg_color="black")

        # Calculate and display differences
        systolic_diff = abs(row["bp_right_sys"] - row["bp_left_sys"]) if pd.notna(row["bp_right_sys"]) and pd.notna(row["bp_left_sys"]) else ""
        diastolic_diff = abs(row["bp_right_dia"] - row["bp_left_dia"]) if pd.notna(row["bp_right_dia"]) and pd.notna(row["bp_left_dia"]) else ""

        if "bp_right_sys - bp_left_sys difference" in deviation_values:
            systolic_diff_label.configure(text=str(systolic_diff), font=("Arial", 12, "bold"), fg_color="red")
        else:
            systolic_diff_label.configure(text=str(systolic_diff), font=("Arial", 12), fg_color="black")

        if "bp_right_dia - bp_left_dia difference" in deviation_values:
            diastolic_diff_label.configure(text=str(diastolic_diff), font=("Arial", 12, "bold"), fg_color="red")
        else:
            diastolic_diff_label.configure(text=str(diastolic_diff), font=("Arial", 12), fg_color="black")

    def next_record():
        if current_index[0] < len(deviating_ids) - 1:
            current_index[0] += 1
            update_display()

    def previous_record():
        if current_index[0] > 0:
            current_index[0] -= 1
            update_display()

    button_frame = ctk.CTkFrame(alerts_window)
    button_frame.pack(side="bottom", pady=10)

    button_previous = ctk.CTkButton(button_frame, text="Previous", command=previous_record, width=100, height=50)
    button_previous.pack(side="left", padx=10)

    button_next = ctk.CTkButton(button_frame, text="Next", command=next_record, width=100, height=50)
    button_next.pack(side="right", padx=10)

    update_display()

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    win.geometry(f"{width}x{height}+{x}+{y}")
