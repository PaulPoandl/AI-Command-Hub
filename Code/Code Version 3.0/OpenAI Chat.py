import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import openai
import webbrowser

class ChatWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("OpenAI Chat")
        self.geometry("700x390")
        self.iconbitmap("ICO Icons/OpenAi.ico")
        self.resizable(False, False)

        self.api_key_entry = ttk.Entry(self)
        self.temperature_entry = ttk.Entry(self)
        self.tokens_entry = ttk.Entry(self)
        self.input_text = scrolledtext.ScrolledText(self, height=10, wrap=tk.WORD,font=("Calibri", 10))
        self.output_text = scrolledtext.ScrolledText(self, height=10, width=80, state=tk.NORMAL, font=("Calibri", 10))

        self.api_key = self.load_api_key()
        self.api_key_entry = ttk.Entry(self)
        self.api_key_entry.insert(0, self.api_key)

        self.create_widgets()

    def create_widgets(self):
        # Entry Section
        api_key_label = ttk.Label(self, text="API Key:")
        temperature_label = ttk.Label(self, text="Temperature:")
        tokens_label = ttk.Label(self, text="Tokens:")

        api_key_label.grid(row=0, column=0, sticky=tk.E, pady=5, padx=5)
        self.api_key_entry.grid(row=0, column=1, sticky=tk.W + tk.E, pady=5, padx=5)

        # Submit Button
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit_api_key)
        self.submit_button.grid(row=0, column=2, pady=5, padx=0)

        # Temperature and Tokens Entry
        temperature_label.grid(row=0, column=3, sticky=tk.E, pady=5, padx=0)
        self.temperature_entry.grid(row=0, column=4, pady=5, padx=5)
        self.temperature_entry.configure(width=8)
        tokens_label.grid(row=0, column=5, sticky=tk.E, pady=5, padx=0)
        self.tokens_entry.grid(row=0, column=6, pady=5, padx=5)
        self.tokens_entry.configure(width=8)

        # Model Selection
        self.model_combobox = ttk.Combobox(self, values=["Ada 001", "Babbage 001", "Curie 001", "Davinci", "Davinci 002", "Davinci 003"])
        self.model_combobox.set("Davinci")
        self.model_combobox.configure(width=12)
        self.model_combobox.grid(row=0, column=8, pady=5, padx=0)

        # Input Section
        self.input_text.grid(row=1, column=0, columnspan=8, pady=5, padx=5)
        self.input_text.insert(tk.END, "Here you have to write your query...\n")

        # Send Button
        self.send_button = ttk.Button(self, text="Send", command=self.send_message, state=tk.DISABLED)
        self.send_button.grid(row=1, column=8, pady=5, padx=5)

        # Output Section
        self.output_text.grid(row=2, column=0, columnspan=8, pady=5, padx=5)
        self.output_text.insert(tk.END, "Here you will see the Model's Answers...\n")

        # Clear Button
        self.clear_button = ttk.Button(self, text="Clear", command=self.clear_output, state=tk.DISABLED)
        self.clear_button.grid(row=2, column=8, pady=5, padx=5)

        # Window Close
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
            "Help: OpenAI Chat\n\n"
            "1. How to Use the Program:\n"
            "   - Enter your OpenAI API key in the 'API Key' field.\n"
            "   - Adjust the 'Temperature' and 'Tokens' values (explained below).\n"
            "   - Choose a model from the dropdown list.\n"
            "   - Type your query in the input box.\n"
            "   - Click 'Submit' to authenticate your API key.\n"
            "   - Once authenticated, you can click 'Send' to receive responses.\n\n"
            "2. Tokens and Temperature:\n"
            "   - Tokens: It controls the length of the response. Higher values generate longer responses. Example: 2000 or 2500\n"
            "   - Temperature: It influences the randomness of the model's output. Higher values make the output more creative, but lower values make it more focused. Example: 1.0 or 1.5\n\n"
            "3. Performance Note:\n"
            "   - This program is designed for educational purposes and may not match the capabilities of Chat GPT. It serves as an exploration of OpenAI's models.\n"
            "   - The program does not remember past communication sessions. Each interaction is independent.\n"
            "   - Note that the program may occasionally break or experience long loading times. Be patient if it takes time to respond.\n"
            "   - Choosing the right model is crucial for getting accurate and relevant answers.\n\n"
            "4. Model Selection:\n"
            "   - Choose from models like 'Ada 001,' 'Babbage 001,' 'Curie 001,' and versions of 'Davinci' (002, 003).\n"
            "   - Each model has a different token limit. Refer to OpenAI's website for specific token limits for each model.\n\n"
            "5. API Key:\n"
            "   - Get your API key from OpenAI. It's free initially, but costs may apply later.\n"
            "   - Visit OpenAI's website (https://beta.openai.com/signup/) to obtain your API key."
        )
        messagebox.showinfo("Help", help_text)


    def open_website(self):
        webbrowser.open("https://aicommandhub2.wordpress.com")

    def show_about_info(self):
        about_text = (
            "OpenAI Chat\n"
            "Version 1.0\n"
            "Developed by ByteGroove Labs\n"
            "© 2023 All rights reserved"
        )
        messagebox.showinfo("About", about_text)

    def load_api_key(self):
        try:
            with open("TXT Files/api_key_OpenAI.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return ""
    
    def save_api_key(self, api_key):
        with open("TXT Files/api_key_OpenAI.txt", "w") as file:
            file.write(api_key)
        
    def clear_output(self):
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.configure(state=tk.DISABLED)

    def submit_api_key(self):
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showwarning("Error", "Please enter an API key.")
            return
        try:
            openai.api_key = api_key
            self.save_api_key(api_key)
            # Test the API key by making a simple request
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt="Test API key",
                max_tokens=5,
            )
            # If successful, enable the buttons
            self.send_button["state"] = tk.NORMAL
            self.clear_button["state"] = tk.NORMAL
        except openai.error.AuthenticationError as e:
            # If there's an authentication error, disable the buttons and show a warning
            self.send_button["state"] = tk.DISABLED
            self.clear_button["state"] = tk.DISABLED
            messagebox.showwarning("Error", "Invalid API key.")
        except Exception as e:
            # Handle other exceptions
            self.send_button["state"] = tk.DISABLED
            self.clear_button["state"] = tk.DISABLED
            messagebox.showwarning("Error", f"An error occurred: {str(e)}")

    def send_message(self):
        # Get user input and selected model
        user_input = self.input_text.get("1.0", tk.END)
        selected_model = self.model_combobox.get()

        if not user_input.strip():
            messagebox.showwarning("Error", "Please enter something before sending.")
            return
        try:
            temperature = float(self.temperature_entry.get())
            tokens = int(self.tokens_entry.get())
        except ValueError:
            messagebox.showwarning("Error", "Please enter valid values for Temperature and Tokens.")
            return

        self.send_button["state"] = tk.DISABLED
        self.clear_output()
        response = chat_with_gpt3(user_input, selected_model, temperature, tokens)
        self.output_text.configure(state=tk.NORMAL)
        self.insert_formatted_text(response)
        self.output_text.configure(state=tk.DISABLED)
        self.send_button["state"] = tk.NORMAL

    def insert_formatted_text(self, response):
        words = response.split()
        line_width = 80
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= line_width:
                current_line += word + " "
            else:
                self.output_text.insert(tk.END, current_line + "\n")
                current_line = word + " "
        if current_line:
            self.output_text.insert(tk.END, current_line + "\n")

    def on_close(self):
        self.destroy()

def chat_with_gpt3(prompt, model_name, temperature, tokens):
    models = {
        "Ada 001": "text-ada-001",
        "Babbage 001": "text-babbage-001",
        "Curie 001": "text-curie-001",
        "Davinci": "davinci",
        "Davinci 002": "text-davinci-002",
        "Davinci 003": "text-davinci-003",
    }
    model = models.get(model_name, "text-davinci-003")
    try:
        completions = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=tokens,
            n=1,
            stop=None,
            temperature=temperature,
        )
        message = completions.choices[0].text
        return message
    except Exception as e:
        return "Error communicating with the GPT-3 model: {}".format(str(e))

if __name__ == '__main__':
    app = ChatWindow()
    app.mainloop()
