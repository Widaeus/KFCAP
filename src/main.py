import customtkinter as ctk
from tkinter import filedialog, messagebox
from reader_prep import import_data
from redcap import Project

ctk.set_appearance_mode("dark")  # Set the appearance mode to dark

def define_url_token_project(api_token):
    api_url = 'https://redcap.ki.se/api/'
    project = Project(api_url, api_token)
    return project

def run_process():
    # Get the inputs from the GUI
    data_path = entry_data_path.get()
    api_token = entry_api_token.get()
    data_form = combo_data_form.get()  

    if not data_path or not api_token or not data_form:
        messagebox.showerror("Error", "All fields must be filled in.")
        return

    # Define REDCap project
    try:
        project = define_url_token_project(api_token)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to REDCap: {e}")
        return

    # Process the data
    try:
      if data_form == "OLO data":
        # Convert and clean data
        sample_ids = import_data(data_path, project)
        messagebox.showinfo("Success", f"The following IDs were successfully imported: {', '.join(sample_ids)}")
      else:
         raise ValueError(f"Data form {data_form} is not supported as of this moment.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during data processing: {e}")

def browse_files():
    filename = filedialog.askdirectory()
    entry_data_path.delete(0, ctk.END)
    entry_data_path.insert(0, filename)

# Create the main window
root = ctk.CTk()
root.title("Data import to REDcap")

# Labels and entry fields
label_data_path = ctk.CTkLabel(root, text="Data Path")
label_data_path.grid(row=0, column=0, padx=10, pady=10)

entry_data_path = ctk.CTkEntry(root, width=300)
entry_data_path.grid(row=0, column=1, padx=10, pady=10)

button_browse = ctk.CTkButton(root, text="Browse", command=browse_files)
button_browse.grid(row=0, column=2, padx=10, pady=10)

label_api_token = ctk.CTkLabel(root, text="API Token")
label_api_token.grid(row=1, column=0, padx=10, pady=10)

entry_api_token = ctk.CTkEntry(root, width=300, show='*')
entry_api_token.grid(row=1, column=1, padx=10, pady=10)

label_data_form = ctk.CTkLabel(root, text="Data Form")
label_data_form.grid(row=2, column=0, padx=10, pady=10)

combo_data_form = ctk.CTkComboBox(root, values=["OLO data", "Echocardiographic data"], width=300)
combo_data_form.grid(row=2, column=1, padx=10, pady=10)
combo_data_form.set("Select Data Form")  # Set default value

# Submit button
button_submit = ctk.CTkButton(root, text="Run", command=run_process)
button_submit.grid(row=3, column=1, padx=10, pady=10)

# Run the main loop
root.mainloop()
