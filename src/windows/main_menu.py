import customtkinter as ctk
from src.utils.utils import clear_window

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
    frame.grid_rowconfigure(1, weight=0)  # Subtitle row
    frame.grid_rowconfigure(2, weight=1)  # Button frame row
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

    # Place the button_frame in the center cell
    button_frame = ctk.CTkFrame(frame)
    button_frame.grid(row=2, column=1, pady=20)

    # Configure button_frame columns
    button_frame.grid_columnconfigure((0, 1, 2), weight=1)

    # Add buttons to button_frame
    button_data_import = ctk.CTkButton(
        button_frame, text="Data import", command=lambda: show_data_import(root)
    )
    button_data_import.grid(row=0, column=0, padx=10, pady=10)

    button_alert_handling = ctk.CTkButton(
        button_frame, text="Alert handling", command=lambda: show_alert_handling(root)
    )
    button_alert_handling.grid(row=0, column=1, padx=10, pady=10)

    button_letter_generation = ctk.CTkButton(
        button_frame, text="Survey to letter", command=lambda: show_letter_generation(root)
    )
    button_letter_generation.grid(row=0, column=2, padx=10, pady=10)
