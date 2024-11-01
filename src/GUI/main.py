import customtkinter as ctk

# Import window configuration functions
from src.windows.main_menu import show_main_menu

ctk.set_appearance_mode("dark")  # Set the appearance mode to dark
entry_api_token = None
combo_data_form = None
root = ctk.CTk()  # Define root
root.title("KFCap v1.0.2")
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

def main():
    show_main_menu(root)
    root.mainloop()