import customtkinter as ctk
from src.utils.utils import validate_api_token, define_url_token_project, clear_window, display_alerts_window

def show_alert_handling(root):
    from src.windows.main_menu import show_main_menu
    
    clear_window(root)
    frame = ctk.CTkFrame(root)
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
    
    # Frame for buttons
    button_frame = ctk.CTkFrame(frame)
    button_frame.grid(row=3, column=0, columnspan=3, pady=20)

    # Run button
    button_run = ctk.CTkButton(
        button_frame, 
        text="Run", 
        command=lambda: display_alerts_window(
            define_url_token_project(entry_api_token.get(), root)
        )
    )
    button_run.pack(side="left", padx=10)

    # Back button
    button_back = ctk.CTkButton(button_frame, text="Back", command=lambda: show_main_menu(root))
    button_back.pack(side="left", padx=10)
