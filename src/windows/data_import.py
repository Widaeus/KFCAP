import customtkinter as ctk
from src.utils.utils import clear_window, browse_files, run_process
from src.models.session_manager import session_manager

def show_data_import(root):
    from src.windows.main_menu import show_main_menu
    
    clear_window(root)
    
    frame = ctk.CTkFrame(root)
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    
    cached_api_token = session_manager.get_api_token()

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
    label_subtitle.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    # Data Path
    label_data_path = ctk.CTkLabel(frame, text="Data Path")
    label_data_path.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    global entry_data_path
    entry_data_path = ctk.CTkEntry(frame, width=300)
    entry_data_path.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    button_browse = ctk.CTkButton(frame, text="Browse", command=lambda: browse_files(entry_data_path))
    button_browse.grid(row=1, column=2, padx=10, pady=10, sticky="w")
    
    # Data Form Selection
    label_data_form = ctk.CTkLabel(frame, text="Data Form")
    label_data_form.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    combo_data_form = ctk.CTkComboBox(frame, values=["OLO data", "Echocardiographic data"], width=300)
    combo_data_form.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    combo_data_form.set("Select Data Form")
    
    # Frame for buttons
    button_frame = ctk.CTkFrame(frame)
    button_frame.grid(row=3, column=0, columnspan=3, pady=20)

    # Run button
    button_run = ctk.CTkButton(button_frame, text="Import", command=lambda: run_process(entry_data_path, combo_data_form))
    button_run.pack(side="left", padx=10)

    # Back button
    button_back = ctk.CTkButton(button_frame, text="Back", command=lambda: show_main_menu(root))
    button_back.pack(side="left", padx=10)