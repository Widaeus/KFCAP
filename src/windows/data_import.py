import customtkinter as ctk
from src.utils.utils import clear_window, validate_api_token, browse_files, run_process

def show_data_import(root):
    from src.windows.main_menu import show_main_menu
    
    clear_window(root)
    
    frame = ctk.CTkFrame(root)
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Data Path
    label_data_path = ctk.CTkLabel(frame, text="Data Path")
    label_data_path.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    global entry_data_path
    entry_data_path = ctk.CTkEntry(frame, width=300)
    entry_data_path.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    button_browse = ctk.CTkButton(frame, text="Browse", command=browse_files)
    button_browse.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    # API Token
    label_api_token = ctk.CTkLabel(frame, text="API Token")
    label_api_token.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    entry_api_token = ctk.CTkEntry(frame, width=300, show='*')
    entry_api_token.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    
    label_validation = ctk.CTkLabel(frame, text="")
    label_validation.grid(row=1, column=2, padx=10, pady=10, sticky="w")

    entry_api_token.bind("<KeyRelease>", lambda event: validate_api_token(entry_api_token.get(), label_validation))

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
    button_run = ctk.CTkButton(button_frame, text="Import", command=lambda: run_process(entry_data_path, entry_api_token, combo_data_form))
    button_run.pack(side="left", padx=10)

    # Back button
    button_back = ctk.CTkButton(button_frame, text="Back", command=lambda: show_main_menu(root))
    button_back.pack(side="left", padx=10)

    frame.grid_rowconfigure(4, weight=1)
