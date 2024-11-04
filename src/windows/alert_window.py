import customtkinter as ctk
import tkinter as tk
from src.utils.utils import clear_window, browse_files, load_csv
from src.utils.parser import alerts_from_df_revised, check_deviations_revised
from src.models.session_manager import session_manager
from src.windows.alert_popup import display_alerts_popup
from src.windows.infobox import show_docs

def show_alert_handling(root):
    from src.windows.main_menu import show_main_menu
    
    clear_window(root)
    frame = ctk.CTkFrame(root, height=600)
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    
    frame.grid_columnconfigure(1, weight=1)
    
    # Title
    label_title = ctk.CTkLabel(frame, text="Alert handling", font=("Arial", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
    
    # Check for cached API token
    cached_api_token = session_manager.get_api_token()

    # Determine the subtitle text based on the presence of the cached API token
    if cached_api_token:
        project_instance = session_manager.get_project_instance()
        project_info = project_instance.export_project_info()
        project_title = project_info.get('project_title', 'Unknown Project')
        subtitle_text = project_title if project_title else "No cached API token"
    else:
        subtitle_text = "No cached API token"

    # Subtitle
    label_subtitle = ctk.CTkLabel(
        frame, 
        text=subtitle_text, 
        font=("Arial", 12),
        text_color="green"
    )
    label_subtitle.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    # Alert conditions file
    label_alert_conditions = ctk.CTkLabel(frame, text="Alert Conditions File")
    label_alert_conditions.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    entry_alert_conditions = ctk.CTkEntry(frame, width=300)
    entry_alert_conditions.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    def load_alert_titles():
        file_path = entry_alert_conditions.get()
        if file_path:
            df = load_csv(file_path)
            alert_titles = df['alert-title'].tolist()
            dropdown_alert_titles.delete(0, tk.END)
            for title in alert_titles:
                dropdown_alert_titles.insert(tk.END, title)

    button_browse = ctk.CTkButton(frame, text="Browse", command=lambda: [browse_files(entry_alert_conditions), load_alert_titles()])
    button_browse.grid(row=2, column=2, padx=10, pady=10, sticky="w")
    
    # Dropdown for alert titles
    label_select_alerts = ctk.CTkLabel(frame, text="Select Alerts")
    label_select_alerts.grid(row=3, column=0, padx=10, pady=10, sticky="e")

    dropdown_alert_titles = tk.Listbox(frame, selectmode='multiple', width=50, height=10, font=("Arial", 20))
    dropdown_alert_titles.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    # Frame for buttons
    button_frame = ctk.CTkFrame(frame)
    button_frame.grid(row=4, column=0, columnspan=3, pady=20)

    # Run button
    def run_alert_handling():
        selected_indices = dropdown_alert_titles.curselection()
        selected_alerts = [dropdown_alert_titles.get(i) for i in selected_indices]
        redcap_data = project_instance.export_records(format_type="df")
        
        file_path = entry_alert_conditions.get()
        csv_df = load_csv(file_path)
        
        filtered_alerts_df = csv_df[csv_df['alert-title'].isin(selected_alerts)]
        
        alerts = alerts_from_df_revised(filtered_alerts_df, project_instance)
        deviating_vars = check_deviations_revised(redcap_data, project_instance)
        
        display_alerts_popup(deviating_vars, alerts, redcap_data, project_instance, root)

    button_run = ctk.CTkButton(
        button_frame, 
        text="Run",
        command=run_alert_handling
    )
    button_run.pack(side="left", padx=10)

    # Back button
    ctk.CTkButton(button_frame, text="Back", command=lambda: show_main_menu(root)).pack(side="left", padx=10)
    
    # Info Button
    info_button = ctk.CTkButton(frame, text="i", width=20, height=20, command=lambda: show_docs(root))
    info_button.grid(row=0, column=2, padx=15, pady=15, sticky="ne")