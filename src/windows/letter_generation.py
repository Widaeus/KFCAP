import customtkinter as ctk
from tkinter import filedialog
from src.utils.utils import validate_api_token, clear_window
from src.windows.infobox import show_docs

def show_letter_generation(root):
    from src.windows.main_menu import show_main_menu
    
    clear_window(root)
    
    # Create and grid the main frame with reduced padding
    frame = ctk.CTkFrame(root)
    frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
    # Configure grid weights to prevent excessive expansion
    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=0)
    
    # Title
    label_title = ctk.CTkLabel(frame, text="Letter Generation", font=("Arial", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=3, padx=5, pady=(5, 10), sticky="ew")

    # Subtitle
    label_subtitle = ctk.CTkLabel(
        frame, 
        text="Generate letters for studies SCAPIS2spectrum and MIND", 
        font=("Arial", 12)
    )
    label_subtitle.grid(row=1, column=0, columnspan=3, padx=5, pady=(0, 10), sticky="ew")

    # API token
    label_api_token = ctk.CTkLabel(frame, text="API Token")
    label_api_token.grid(row=2, column=0, padx=5, pady=5, sticky="e")

    entry_api_token = ctk.CTkEntry(frame, width=200, show='*')
    entry_api_token.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    label_validation = ctk.CTkLabel(frame, text="", text_color="red")
    label_validation.grid(row=2, column=2, padx=5, pady=5, sticky="w")

    entry_api_token.bind(
        "<KeyRelease>", 
        lambda event: validate_api_token(entry_api_token.get(), label_validation)
    )
    
    # File browse for letter template
    label_letter_template = ctk.CTkLabel(frame, text="Letter Template File")
    label_letter_template.grid(row=3, column=0, padx=5, pady=5, sticky="e")

    entry_letter_template = ctk.CTkEntry(frame, width=200)
    entry_letter_template.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    def browse_letter_template():
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
        )
        if file_path:
            entry_letter_template.delete(0, ctk.END)
            entry_letter_template.insert(0, file_path)

    button_browse_letter_template = ctk.CTkButton(
        frame, 
        text="Browse", 
        command=browse_letter_template
    )
    button_browse_letter_template.grid(row=3, column=2, padx=5, pady=5, sticky="w")

    # File browse for key
    label_key = ctk.CTkLabel(frame, text="Key File")
    label_key.grid(row=4, column=0, padx=5, pady=5, sticky="e")

    entry_key = ctk.CTkEntry(frame, width=200)
    entry_key.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    def browse_key_file():
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
        )
        if file_path:
            entry_key.delete(0, ctk.END)
            entry_key.insert(0, file_path)

    button_browse_key = ctk.CTkButton(
        frame, 
        text="Browse", 
        command=browse_key_file
    )
    button_browse_key.grid(row=4, column=2, padx=5, pady=5, sticky="w")
    
    # Run button to initiate letter generation
    button_run = ctk.CTkButton(
        frame, 
        text="Run", 
        command=lambda: generate_letters(
            entry_api_token.get(), 
            entry_letter_template.get(), 
            entry_key.get()
        )
    )
    button_run.grid(row=5, column=1, padx=5, pady=10, sticky="e")
    
    # Back button
    button_back = ctk.CTkButton(frame, text="Back", command=lambda: show_main_menu(root))
    button_back.grid(row=5, column=2, padx=5, pady=10, sticky="w")

    # Info Button
    info_button = ctk.CTkButton(frame, text="i", width=20, height=20, command=lambda: show_docs(root))
    info_button.grid(row=0, column=2, padx=15, pady=15, sticky="ne")