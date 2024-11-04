import os
from tkinter import Toplevel
from tkinterweb import HtmlFrame
import markdown

def show_docs(root):
    docs_window = Toplevel(root)
    docs_window.title("Documentation")
    
    default_width = 1200
    default_height = 1600
    docs_window.geometry(f"{default_width}x{default_height}")
    docs_window.minsize(300, 200)  # Set a minimum size


    # Read and convert the contents of docs/usage.md to HTML
    docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'usage.md'))
    try:
        with open(docs_path, 'r') as file:
            md_content = file.read()
            html_content = markdown.markdown(md_content)
            # Add CSS to make the text larger
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <style>
                body {{
                    font-size: 30px;
                }}
                h1 {{
                    font-size: 40px;
                }}
                h2 {{
                    font-size: 36px;
                }}
                h3 {{
                    font-size: 32px;
                }}
            </style>
            </head>
            <body>
            {html_content}
            </body>
            </html>
            """
    except FileNotFoundError:
        html_content = "<h1>Documentation file not found.</h1>"

    # Display the HTML content in an HtmlFrame
    html_frame = HtmlFrame(docs_window, horizontal_scrollbar="auto", messages_enabled = False)
    html_frame.load_html(html_content)
    html_frame.pack(expand=True, fill='both')
    
    docs_window.update_idletasks()
    content_width = html_frame.winfo_reqwidth()
    content_height = html_frame.winfo_reqheight()
    new_width = max(default_width, content_width)
    new_height = max(default_height, content_height)
    docs_window.geometry(f"{new_width}x{new_height}")
    docs_window.resizable(True, True)