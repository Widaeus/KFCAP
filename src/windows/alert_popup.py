
import customtkinter as ctk
import pandas as pd
from src.utils.utils import find_study_id
from src.utils.utils import center_window
from src.windows.infobox import show_docs

def display_alerts_popup(deviating_vars, alerts, redcap_data, project_instance, root):
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