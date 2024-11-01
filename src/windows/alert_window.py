import customtkinter as ctk
import tkinter as tk
from src.utils.utils import validate_api_token, define_url_token_project, clear_window, display_alerts_window, browse_files
from src.utils.alert_handling import load_csv, find_deviating_records

def show_alert_handling(root):
    from src.windows.main_menu import show_main_menu
    
    clear_window(root)
    frame = ctk.CTkFrame(root, height=600)
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    
    frame.grid_columnconfigure(1, weight=1)
    
    # Title
    label_title = ctk.CTkLabel(frame, text="Alert handling", font=("Arial", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Subtitle
    label_subtitle = ctk.CTkLabel(
        frame, 
        text="As of this version only compatible with studies SCAPIS2spectrum and MIND", 
        font=("Arial", 12)
    )
    label_subtitle.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    # API token
    label_api_token = ctk.CTkLabel(frame, text="API Token")
    label_api_token.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    entry_api_token = ctk.CTkEntry(frame, width=300, show='*')
    entry_api_token.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    
    label_validation = ctk.CTkLabel(frame, text="")
    label_validation.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    entry_api_token.bind(
        "<KeyRelease>", 
        lambda event: validate_api_token(entry_api_token.get(), label_validation)
    )
    
    # Alert conditions file
    label_alert_conditions = ctk.CTkLabel(frame, text="Alert Conditions File")
    label_alert_conditions.grid(row=3, column=0, padx=10, pady=10, sticky="e")

    entry_alert_conditions = ctk.CTkEntry(frame, width=300)
    entry_alert_conditions.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    def load_alert_titles():
        file_path = entry_alert_conditions.get()
        if file_path:
            df = load_csv(file_path)
            alert_titles = df['alert-title'].tolist()
            dropdown_alert_titles.delete(0, tk.END)
            for title in alert_titles:
                dropdown_alert_titles.insert(tk.END, title)

    button_browse = ctk.CTkButton(frame, text="Browse", command=lambda: [browse_files(entry_alert_conditions), load_alert_titles()])
    button_browse.grid(row=3, column=2, padx=10, pady=10, sticky="w")
    
    # Dropdown for alert titles
    label_select_alerts = ctk.CTkLabel(frame, text="Select Alerts")
    label_select_alerts.grid(row=4, column=0, padx=10, pady=10, sticky="e")

    dropdown_alert_titles = tk.Listbox(frame, selectmode='multiple', width=50, height=10, font=("Arial", 20))
    dropdown_alert_titles.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    # Frame for buttons
    button_frame = ctk.CTkFrame(frame)
    button_frame.grid(row=5, column=0, columnspan=3, pady=20)

    # Run button
    def run_alert_handling():
        selected_indices = dropdown_alert_titles.curselection()
        selected_alerts = [dropdown_alert_titles.get(i) for i in selected_indices]
        file_path = entry_alert_conditions.get()
        df = load_csv(file_path)
        selected_conditions = df[df['alert-title'].isin(selected_alerts)]['alert-condition'].tolist()
        project = define_url_token_project(entry_api_token.get())
        records_info = find_deviating_records(project, selected_conditions)
        display_alerts_window(records_info, root)

    button_run = ctk.CTkButton(
        button_frame, 
        text="Run",
        command=run_alert_handling
    )
    button_run.pack(side="left", padx=10)

    # Back button
    ctk.CTkButton(button_frame, text="Back", command=lambda: show_main_menu(root)).pack(side="left", padx=10)
