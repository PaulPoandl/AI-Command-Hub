import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Toplevel
import wolframalpha
import requests
import webbrowser

class ChatWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("WolframAlpha Chat")
        self.geometry("470x390")
        self.resizable(False, False)
        self.iconbitmap("ICO Icons/WolframAlpha.ico")

        self.app_id_entry = ttk.Entry(self)
        self.input_text = scrolledtext.ScrolledText(self, height=10, width=50, wrap=tk.WORD, font=("Calibri", 10))
        self.output_text = scrolledtext.ScrolledText(self, height=10, width=50, state=tk.NORMAL, font=("Calibri", 10))

        self.app_id = self.load_app_id()
        self.app_id_entry.insert(0, self.app_id)

        self.create_widgets()

    def create_widgets(self):
        app_id_label = ttk.Label(self, text="App ID:")
        app_id_label.grid(row=0, column=0, sticky=tk.E, pady=5, padx=0)
        self.app_id_entry.grid(row=0, column=1, sticky=tk.W + tk.E, pady=5, padx=0)

        self.submit_button = ttk.Button(self, text="Submit", command=self.submit_app_id)
        self.submit_button.grid(row=0, column=2, pady=5, padx=0)
        self.math_button_window_button = ttk.Button(self, text="Math Buttons", command=self.open_math_button_window)
        self.math_button_window_button.grid(row=0, column=3, pady=5, padx=0)

        self.input_text.grid(row=1, column=0, columnspan=3, pady=5, padx=5)
        self.input_text.insert(tk.END, "Here you have to write your query...\n")
        self.output_text.grid(row=2, column=0, columnspan=3, pady=5, padx=5)
        self.output_text.insert(tk.END, "Here you will see the answers...\n")

        self.send_button = ttk.Button(self, text="Send", command=self.send_message, state=tk.DISABLED)
        self.send_button.grid(row=1, column=3, pady=5, padx=2)
        self.clear_button = ttk.Button(self, text="Clear", command=self.clear_output, state=tk.DISABLED)
        self.clear_button.grid(row=2, column=3, pady=5, padx=2)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Create a Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        menubar.add_cascade(label="Help", menu=help_menu)

        # About Menu
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="About", command=self.show_about_info)
        menubar.add_cascade(label="About", menu=about_menu)

        # Website Button
        website_menu = tk.Menu(menubar, tearoff=0)
        website_menu.add_command(label="Website", command=self.open_website) 
        menubar.add_cascade(label="Website", menu=website_menu)

    def show_help(self):
        help_text = (
        "Help: WolframAlpha Chat\n\n"
        "1. How to Use the Program:\n"
        "   - Obtain your Wolfram Alpha API key from their website.\n"
        "   - Visit (https://developer.wolframalpha.com) to get your API key.\n"
        "   - Enter your Wolfram Alpha API key in the 'App ID' field.\n"
        "   - Click 'Submit' to authenticate your API key.\n"
        "   - Once authenticated, you can type your query in the input box.\n"
        "   - Click 'Send' to send the query and receive responses.\n"
        "   - Use 'Clear' to clear the output window.\n"
        "   - Optionally, you can explore 'Math Buttons' for quick expression input.\n\n"
        "2. Math Buttons:\n"
        "   - Math Buttons provide quick input for common mathematical expressions.\n"
        "   - Clicking on a button inserts the corresponding expression into the input box.\n\n"
        "3. Important Note:\n"
        "   - This program utilizes Wolfram Alpha's API for computations.\n"
        "   - Wolfram Alpha is an external service, and you must obtain your own API key.\n"
        "   - Ensure you follow Wolfram Alpha's guidelines for API usage.\n"
        "   - Be aware of regulatory considerations regarding AI usage, such as monthly limits.\n"
        "   - Visit Wolfram Alpha's official website (https://wolframalpha.com) for API details.\n"
        "   - Note that Wolfram Alpha's API has its own limitations and usage policies.\n\n"
        "4. Menus:\n"
        "   - 'Help': Access help information about the program.\n"
        "   - 'About': View information about the program's version and development.\n"
        "   - 'Website': Open the program's official website for additional resources.\n\n"
        "5. Note:\n"
        "   - Ensure a stable internet connection for Wolfram Alpha queries.\n"
        "   - In case of issues, check for error messages in the output window.\n"
        "   - Visit the official website for updates and support: (https://aicommandhub2.wordpress.com)"
        )
        messagebox.showinfo("Help", help_text)
    
    def open_website(self):
        webbrowser.open("https://aicommandhub2.wordpress.com")

    def show_about_info(self):
        about_text = (
            "WolframAlpha Chat\n"
            "Version 1.0\n"
            "Developed by ByteGroove Labs\n"
            "© 2023 All rights reserved"
        )
        messagebox.showinfo("About", about_text)

    def load_app_id(self):
        try:
            with open("TXT Files/app_id_WolframAlpha.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return ""
    def save_app_id(self, app_id):
        with open("TXT Files/app_id_WolframAlpha.txt", "w") as file:
            file.write(app_id)
    def clear_output(self):
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.configure(state=tk.DISABLED)
    def validate_api_key(self, app_id):
        try:
            client = wolframalpha.Client(app_id)
            # Make a test request to validate the API key
            test_query = client.query("Test")
            next(test_query.results)
            return True
        except Exception:
            return False
    def submit_app_id(self):
        app_id = self.app_id_entry.get().strip()
        if not app_id:
            messagebox.showwarning("Error", "Please enter an App ID.")
            return
        if not self.validate_api_key(app_id):
            messagebox.showwarning("Error", "Invalid Wolfram Alpha API Key.")
            self.send_button["state"] = tk.DISABLED
            self.clear_button["state"] = tk.DISABLED
            return
        try:
            self.client = wolframalpha.Client(app_id)
            self.save_app_id(app_id)
            self.send_button["state"] = tk.NORMAL
            self.clear_button["state"] = tk.NORMAL
        except Exception as e:
            self.send_button["state"] = tk.DISABLED
            self.clear_button["state"] = tk.DISABLED
            messagebox.showwarning("Error", f"An error occurred: {str(e)}")
    def insert_expression(self, expression):
        self.input_text.insert(tk.END, expression)
    def send_message(self):
        user_input = self.input_text.get("1.0", tk.END)
        self.send_button["state"] = tk.DISABLED
        self.clear_output()
        response = chat_with_wolframalpha(user_input)
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.insert(tk.END, response)
        self.output_text.configure(state=tk.DISABLED)
        self.send_button["state"] = tk.NORMAL
    def on_close(self):
        self.destroy()
    def open_math_button_window(self):
        math_button_window = Toplevel(self)
        MathButtonWindow(math_button_window, self.insert_expression)


class MathButtonWindow:
    def __init__(self, master, insert_function):
        self.master = master
        self.insert_function = insert_function
        self.master.iconbitmap("ICO Icons/WolframAlpha.ico")
        self.master.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        math_buttons = [
            ("sin", lambda: self.insert_expression("sin(")),
            ("cos", lambda: self.insert_expression("cos(")),
            ("tan", lambda: self.insert_expression("tan(")),
            ("asin", lambda: self.insert_expression("asin(")),
            ("acos", lambda: self.insert_expression("acos(")),
            ("atan", lambda: self.insert_expression("atan(")),
            ("sqrt", lambda: self.insert_expression("sqrt(")),
            ("log", lambda: self.insert_expression("log(")),
            ("exp", lambda: self.insert_expression("exp(")),
            ("abs", lambda: self.insert_expression("abs(")),
            ("floor", lambda: self.insert_expression("floor(")),
            ("ceil", lambda: self.insert_expression("ceil(")),
            ("derivative", lambda: self.insert_expression("derivative(")),
            ("pi", lambda: self.insert_expression("pi")),
            ("e", lambda: self.insert_expression("e")),
            ("^", lambda: self.insert_expression("^")),
            ("!", lambda: self.insert_expression("!")),
            ("7", lambda: self.insert_expression("7")),
            ("8", lambda: self.insert_expression("8")),
            ("9", lambda: self.insert_expression("9")),
            ("/", lambda: self.insert_expression("/")),
            ("4", lambda: self.insert_expression("4")),
            ("5", lambda: self.insert_expression("5")),
            ("6", lambda: self.insert_expression("6")),
            ("*", lambda: self.insert_expression("*")),
            ("1", lambda: self.insert_expression("1")),
            ("2", lambda: self.insert_expression("2")),
            ("3", lambda: self.insert_expression("3")),
            ("-", lambda: self.insert_expression("-")),
            ("0", lambda: self.insert_expression("0")),
            (".", lambda: self.insert_expression(".")),
            ("(", lambda: self.insert_expression("(")),
            (")", lambda: self.insert_expression(")")),
            ("+", lambda: self.insert_expression("+")),
            ("%", lambda: self.insert_expression("%")),
            ("=", lambda: self.insert_expression("=")),
        ]

        row, col = 0, 0
        for text, command in math_buttons:
            ttk.Button(self.master, text=text, command=command, style="Modern.TButton").grid(row=row, column=col, pady=3, padx=3)
            col += 1
            if col > 3:
                col = 0
                row += 1
                
    def insert_expression(self, expression):
        self.insert_function(expression)
    def send_message(self):
            self.master.destroy()

def chat_with_wolframalpha(query):
    try:
        response = app.client.query(query)
        if response.success:
            result = next(response.results).text
            return result
        else:
            return f"Wolfram Alpha query failed with error code: {response.error.code}, details: {response.error.msg}"
    except StopIteration:
        return "No results found for the query."
    except (ConnectionError, TimeoutError) as network_error:
        return f"Network error: {str(network_error)}"
    except requests.exceptions.RequestException as request_error:
        return f"Request error: {str(request_error)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


if __name__ == '__main__':
    app = ChatWindow()
    app.mainloop()
