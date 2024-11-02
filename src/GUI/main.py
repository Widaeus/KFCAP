import customtkinter as ctk

# Import window configuration functions
from src.windows.main_menu import show_main_menu
from src.models.session_manager import session_manager

ctk.set_appearance_mode("dark")
entry_api_token = None
combo_data_form = None
root = ctk.CTk()
root.title("KFCap v1.0.2")
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

def main():
    show_main_menu(root)
    root.mainloop()

if __name__ == "__main__":
    main()