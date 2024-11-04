import customtkinter as ctk
import os
from src.utils.utils import clear_window, validate_api_token
from src.models.session_manager import session_manager
from src.models.project import redcapProj
from src.windows.infobox import show_docs

def show_main_menu(root):
    from src.windows.data_import import show_data_import
    from src.windows.alert_window import show_alert_handling
    from src.windows.letter_generation import show_letter_generation
    
    clear_window(root)

    frame = ctk.CTkFrame(root)
    frame.grid(row=0, column=0, sticky="nsew")

    # Configure the root window and main frame to expand
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Configure rows and columns in the main frame
    frame.grid_rowconfigure(0, weight=1)  # Title row
    frame.grid_rowconfigure(1, weight=1)  # Subtitle row
    frame.grid_rowconfigure(2, weight=1)  # API Token row
    frame.grid_rowconfigure(3, weight=1)  # Button frame row
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)

    # Title
    label_title = ctk.CTkLabel(
        frame, 
        text="KFCAP - REDCap tool for KFC", 
        font=("Arial", 20, "bold")
    )
    label_title.grid(row=0, column=0, columnspan=3, padx=10, pady=(20, 10), sticky="n")

    # Subtitle
    label_subtitle = ctk.CTkLabel(
        frame, 
        text="Welcome to the REDCap tool designed for KFC research studies. Please read the description before use.", 
        font=("Arial", 12)
    )
    label_subtitle.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 20), sticky="n")

    # API Token
    label_api_token = ctk.CTkLabel(frame, text="API Token")
    label_api_token.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    entry_api_token = ctk.CTkEntry(frame, width=300, show='*')
    entry_api_token.grid(row=2, column=1, padx=0, pady=0, sticky="w")
    
    label_validation = ctk.CTkLabel(frame, text="")
    label_validation.grid(row=2, column=2, padx=0, pady=0, sticky="w")

    def on_api_token_change(event):
        api_token = entry_api_token.get()
        if not api_token:
            is_valid = False
        else:
            is_valid = validate_api_token(api_token, label_validation)
        
        button_data_import.configure(state="normal" if is_valid else "disabled", fg_color="green" if is_valid else "transparent")
        button_alert_handling.configure(state="normal" if is_valid else "disabled", fg_color="green" if is_valid else "transparent")
        button_letter_generation.configure(state="normal" if is_valid else "disabled", fg_color="green" if is_valid else "transparent")

        if is_valid:
            session_manager.set_api_token(api_token)
            project_instance = redcapProj(api_url='https://redcap.ki.se/api/', api_token=api_token)
            session_manager.set_project_instance(project_instance)

    entry_api_token.bind("<KeyRelease>", on_api_token_change)
    
    # Place the button_frame in the center cell
    button_frame = ctk.CTkFrame(frame)
    button_frame.grid(row=3, column=0, columnspan=3, pady=10)

    # Configure button_frame columns
    button_frame.grid_columnconfigure((0, 1, 2), weight=1)

    # Add buttons to button_frame
    button_data_import = ctk.CTkButton(
        button_frame, text="Data import", command=lambda: show_data_import(root), state="disabled", fg_color="transparent"
    )
    button_data_import.grid(row=0, column=0, padx=10, pady=10)

    button_alert_handling = ctk.CTkButton(
        button_frame, text="Alert handling", command=lambda: show_alert_handling(root), state="disabled", fg_color="transparent"
    )
    button_alert_handling.grid(row=0, column=1, padx=10, pady=10)

    button_letter_generation = ctk.CTkButton(
        button_frame, text="Survey to letter", command=lambda: show_letter_generation(root), state="disabled", fg_color="transparent"
    )
    button_letter_generation.grid(row=0, column=2, padx=10, pady=10)

    # Check for cached API token
    cached_api_token = session_manager.get_api_token()
    if cached_api_token:
        entry_api_token.insert(0, cached_api_token)
        is_valid = validate_api_token(cached_api_token, label_validation)
        button_data_import.configure(state="normal" if is_valid else "disabled", fg_color="green" if is_valid else "transparent")
        button_alert_handling.configure(state="normal" if is_valid else "disabled", fg_color="green" if is_valid else "transparent")
        button_letter_generation.configure(state="normal" if is_valid else "disabled", fg_color="green" if is_valid else "transparent")

    # Info Button
    info_button = ctk.CTkButton(frame, text="i", width=20, height=20, command=lambda: show_docs(root))
    info_button.grid(row=0, column=2, padx=15, pady=15, sticky="ne")