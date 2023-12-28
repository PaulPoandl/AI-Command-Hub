# Import
import time
import datetime
import subprocess
import os
import requests
import json
import webbrowser
import pyttsx3
import speech_recognition as sr
import customtkinter
import tkinter
import tkinter as tk
from tkinter import ttk, PhotoImage, Entry, Label, Tk, Button
from ctypes import windll
from ecapture import ecapture as ec
import wolframalpha
import pyjokes
import keyboard
import pyaudio
from pynput import keyboard
import re
import pywhatkit
import wikipedia
from fuzzywuzzy import fuzz, process
import random
from PIL import Image




# GUI 1
root = customtkinter.CTk()
root.title("AI Command Hub")
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root.geometry("440x180")
root.resizable(False, False)
root.after(201, lambda :root.iconbitmap('ICO Icons/AI-Command-Hub.ico'))
gui_frame = tk.Frame(root, width=400, height=400, bg='grey11')
button_frame = tk.Frame(root, width=400, height=400, bg='grey11')
gui_frame.grid(row=0, column=0, sticky='nsew')
button_frame.grid(row=1, column=0, sticky='nsew')




# Variables
engine = pyttsx3.init()
r = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
volume = engine.getProperty('rate')
engine.setProperty('rate', 145)
volume = engine.getProperty('volume')
engine.setProperty('volume', 1.0)
is_muted = False




# Button Functions
def speak(text):
    engine.say(text)
    engine.runAndWait()
def clear_output():
    output_text.delete(1.0, tk.END)
def open_help_window():
    help = customtkinter.CTk()
    help.after(300, lambda :help.iconbitmap('ICO Icons/AI-Command-Hub Help.ico'))
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    help.grid_rowconfigure(0, weight=1)
    help.grid_columnconfigure(0, weight=1)
    help.title("AI Command Hub - Help")
    tk_textbox = tkinter.Text(help, highlightthickness=0)
    tk_textbox.grid(row=0, column=0, sticky="nsew")
    tk_textbox.configure(bg='black')
    tk_textbox.configure(fg='white')
    with open('TXT Files/Introduction.txt', 'r') as file:
        file_contents = file.read()
    tk_textbox.insert('1.0', file_contents)
    ctk_textbox_scrollbar = customtkinter.CTkScrollbar(help, command=tk_textbox.yview)
    ctk_textbox_scrollbar.grid(row=0, column=1, sticky="ns")
    tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)
    help.mainloop()
def open_Tools_window():
    file_path = 'AI Command Hub - Tools.py'
    try:
        os.startfile(file_path)
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
def mute():
    global is_muted
    is_muted = not is_muted
    if is_muted:
        mute_button.configure(image=unimage,text="")
    else:
        mute_button.configure(image=muimage, text="")
def on_speak_button_click():
    global listen_state
    if listen_state == False:
        listen_state = True
        start_listening()
    else:
        listen_state = False
        stop_listening()
def start_listening():
    global r
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            command_entry.delete(0, tk.END)
            command_entry.insert(0, text)
        except:
            print("Sorry, I didn't catch that.")
def stop_listening():
    r.pause_threshold = 0.8
    r.non_speaking_duration = 0.5
    r.dynamic_energy_threshold = False
    r.dynamic_energy_adjustment_damping = 0.15
    r.dynamic_energy_adjustment_ratio = 1.5




# Main Functions and Programm Logic
commands = {
    "play": ["song", "band", "video"],
    "talk": ["WolframAlpha Chat", "OpenAI Chat"],
    "open": ["youtube", "google", "gmail", "spotify", "microsoft office", "netflix","amazon"],
    "tell me": ["time", "date", "joke"],
    "who is": [],
    "what is": [],
    "who are": [],
    "what are": [],
    "search browser for": [],
    "search wikipedia for": [],
}
def check_input():
    command = command_entry.get()
    if command:
        execute_command_with_input(command)
        command_entry.delete(0, 'end')
    else:
        print("Please enter a command")
        speak("Please enter a command")        
root.bind('<Return>', lambda event: check_input())
def execute_command_with_input(command):
    if command is None:
        command = command_entry.get()
    command_parts = command.split()
    main_command = command_parts[0].lower()
    closest_command = get_closest_match(main_command, commands)
    if main_command in commands:
        execute_command(command)
    else:
        if main_command == "play":
            play_music(command)
        elif main_command == "talk" or main_command == "start":
            talk_to_ai(command)
        elif main_command == "open":
            open_website(command)
        elif main_command == "tell":
            tell_me(command)
        elif main_command == "who" or main_command == "what":
            search_wikipedia(command)
        elif main_command == "search":
            search_browser(command)
        else:
            if closest_command:
                execute_command(closest_command)
            else:
                allday_conversation(command)
def execute_command(command):
    command_parts = command.split()
    main_command = command_parts[0].lower()
    if main_command == "play":
        play_music(command)
    elif main_command == "talk" or main_command == "start":
        talk_to_ai(command)
    elif main_command == "open":
        open_website(command)
    elif main_command == "tell":
        tell_me(command)
    elif main_command == "who" or main_command == "what":
        search_wikipedia(command)
    elif main_command == "search":
        search_browser(command)
def get_closest_match(query, command_dict, threshold=75):
    best_match = None
    best_match_score = -1
    try:
        for command, options in command_dict.items():
            for option in options:
                score = fuzz.token_sort_ratio(query, option)
                if score > best_match_score:
                    best_match_score = score
                    best_match = f"{command} {option}"
        if best_match_score >= threshold:
            return best_match
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None    
def allday_conversation(command):
    custom_commands = {}
    with open("TXT Files/allday_commands.txt", "r", encoding="utf-8", errors="replace") as file:
        for line_number, line in enumerate(file, 1):
            try:
                line = line.strip()
                if line:
                    c, r = line.split(" = ", 1)
                    custom_commands[c] = r
            except UnicodeDecodeError as e:
                print(f"Error on line {line_number}: {e}")
                print(f"Problematic line: {line}")
    if command in custom_commands:
        response = custom_commands[command]
        if not is_muted:
            speak(response)
            output_text.insert(tk.END, f"Assistant: {response}\n")
            command_entry.delete(0, 'end')
        return
    else:
        max_score = -1
        closest_match = None
        for c, r in custom_commands.items():
            input_tokens = command.split()
            custom_command_tokens = c.split()
            token_scores = [fuzz.token_sort_ratio(input_token, custom_token) for input_token in input_tokens for custom_token in custom_command_tokens]
            command_score = sum(token_scores) / len(token_scores)
            if command_score > max_score:
                max_score = command_score
                closest_match = r
        if max_score >= 40:
            response = closest_match
            if not is_muted:
                speak(response)
            output_text.insert(tk.END, f"Assistant: {response}\n")
            command_entry.delete(0, 'end')
            return
        else:
            response = conversation(command) 
def conversation(command):
    responses = [
        "I'm sorry, I didn't understand that.",
        "Could you please rephrase your command?",
        "I'm here to assist you. What can I do for you?"
    ]
    response = random.choice(responses)
    if not is_muted:
        speak(response)
    output_text.insert(tk.END, f"Assistant: {response}\n")
    command_entry.delete(0, 'end')
    return




# Command Functions
def play_music(command):
    query = re.sub(r"play (song|band|video) ", "", command)
    if query:
        if not is_muted:
            speak(f"Playing your demand")
        pywhatkit.playonyt(query)
        output_text.insert(tk.END, f"Playing your demand!\n")
        command_entry.delete(0, 'end')
def talk_to_ai(command):
    ai = re.sub(r"(talk to|start|talk) ", "", command)
    ai = ai.strip()  
    app = ai + ".py"
    try:
        subprocess.Popen(['python', app])
        if not is_muted:
            speak(f"Opening {ai}")
        output_text.insert(tk.END, f"Opening: {ai}\n")
        command_entry.delete(0, 'end')
    except FileNotFoundError:
        if not is_muted:
            speak(f"Failed to start {ai}. Make sure the script exists.")
        output_text.insert(tk.END, f"Failed to start {ai}. Make sure the script exists.\n")
        command_entry.delete(0, 'end')
def open_website(command):
    website = re.sub(r"open ", "", command)
    common_domains = ["youtube", "google", "gmail", "spotify", "microsoft office", "netflix", "amazon"]
    if any(domain in command for domain in common_domains):
        webbrowser.open_new_tab(f"https://www.{website}.com")
    else:
        webbrowser.open_new_tab(f"https://www.{website}")
    if not is_muted:
        speak(f"Opening {website}")
    output_text.insert(tk.END, f"Opening: {website.capitalize()}\n")
    command_entry.delete(0, 'end')
def tell_me(command):
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        if not is_muted:
            speak(f"The time is {current_time}")
        output_text.insert(tk.END, f"Time: {current_time}\n")
        command_entry.delete(0, 'end')
    elif "date" in command:
        current_date = datetime.date.today().strftime("%B %d, %Y")
        if not is_muted:
            speak(f"Today is {current_date}")
        output_text.insert(tk.END, f"Date: {current_date}\n")
        command_entry.delete(0, 'end')
    elif "joke" in command:
        joke = pyjokes.get_joke()
        if not is_muted:
            speak(joke)
        output_text.insert(tk.END, f"Joke: {joke}\n")
        command_entry.delete(0, 'end')
def search_wikipedia(command):
    query = re.sub(r"(who is|what is|who are|what are) ", "", command)
    try:
        result = wikipedia.summary(query, sentences=1)
        if not is_muted:
            speak(f"Here is what I found on {query}: {result}")
        output_text.insert(tk.END, f"{query.capitalize()}: {result}\n")
        command_entry.delete(0, 'end')
    except:
        if not is_muted:
            speak(f"I couldn't find information on {query}. Please try another query.")
        output_text.insert(tk.END, f"Couldn't find information on {query}. Try another query.\n")
        command_entry.delete(0, 'end')
def search_browser(command):
    query = re.sub(r"search (browser|wikipedia) for ", "", command)
    if "wikipedia" in command:
        try:
            result = wikipedia.summary(query, sentences=1)
            if not is_muted:
                speak(f"Here is what I found on {query}: {result}")
            output_text.insert(tk.END, f"{query.capitalize()}: {result}\n")
            command_entry.delete(0, 'end')
        except:
            if not is_muted:
                speak(f"I couldn't find information on {query}. Please try another query.")
            output_text.insert(tk.END, f"Couldn't find information on {query}. Try another query.\n")
            command_entry.delete(0, 'end')
    else:    
        webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
        if not is_muted:
            speak("Here are your search results")
        output_text.insert(tk.END, "Your search results are open\n")
        command_entry.delete(0, 'end')




# GUI 2
command_label1 = customtkinter.CTkLabel(gui_frame, text="       ")
command_label1.grid(row=1, column=1)
command_label2 = customtkinter.CTkLabel(gui_frame, text="       ")
command_label2.grid(row=1, column=4)
command_label3 = customtkinter.CTkLabel(gui_frame, text="", width=5, height=2)
command_label3.grid(row=0, column=1)
command_label4 = customtkinter.CTkLabel(button_frame, text="", width=5, height=2)
command_label4.grid(row=1, column=1)
command_label5 = customtkinter.CTkLabel(button_frame, text="", width=5, height=2)
command_label5.grid(row=3, column=1)
command_label6 = customtkinter.CTkLabel(button_frame, text=" ")
command_label6.grid(row=2, column=11)
command_label7 = customtkinter.CTkLabel(button_frame, text="                         ")
command_label7.grid(row=2, column=1)
command_label8 = customtkinter.CTkLabel(button_frame, text=" ")
command_label8.grid(row=2, column=3)
command_label9 = customtkinter.CTkLabel(button_frame, text=" ")
command_label9.grid(row=2, column=5)
command_label10 = customtkinter.CTkLabel(button_frame, text=" ")
command_label10.grid(row=2, column=9)
command_label11 = customtkinter.CTkLabel(button_frame, text=" ")
command_label11.grid(row=2, column=7)
command_label12 = customtkinter.CTkLabel(button_frame, text=" ")
command_label12.grid(row=2, column=13)

command_entry = customtkinter.CTkEntry(gui_frame, width=200, height=120, placeholder_text="Enter your Command...")
command_entry.grid(row=1, column=2)
output_text = customtkinter.CTkTextbox(gui_frame, width=200, height=120)
output_text.grid(row=1, column=3)
output_text.insert(tk.END, f"Here you will see AI Command   Hub's answers...\n")

muimage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Mute Button.png"),
                                  dark_image=Image.open("PNG Buttons/Mute Button.png"),
                                  size=(15, 15))
unimage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Unmute Button.png"),
                                  dark_image=Image.open("PNG Buttons/Unmute Button.png"),
                                  size=(15, 15))
eimage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Execute Button.png"),
                                  dark_image=Image.open("PNG Buttons/Execute Button.png"),
                                  size=(15, 15))
simage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Speak Button.png"),
                                  dark_image=Image.open("PNG Buttons/Speak Button.png"),
                                  size=(15, 15))
pimage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Submit Button.png"),
                                  dark_image=Image.open("PNG Buttons/Submit Button.png"),
                                  size=(15, 15))
cimage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Clear Button.png"),
                                  dark_image=Image.open("PNG Buttons/Clear Button.png"),
                                  size=(15, 15))
himage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Help Button.png"),
                                  dark_image=Image.open("PNG Buttons/Help Button.png"),
                                  size=(15, 15))
timage =customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Tools Button.png"),
                                  dark_image=Image.open("PNG Buttons/Tools Button.png"),
                                  size=(15, 15))

execute_button = customtkinter.CTkButton(button_frame, image=eimage, text="", command=lambda: execute_command_with_input(command_entry.get()),  width=20, height=20, border_width=0, corner_radius=400)
execute_button.grid(row=2, column=2)
listen_state = False
speak_button = customtkinter.CTkButton(button_frame, image=simage, text="", command=on_speak_button_click, width=20, height=20, border_width=0, corner_radius=400)
speak_button.grid(row=2, column=6)
submit_button = customtkinter.CTkButton(button_frame, image=pimage, text="", command=check_input, width=20, height=20, border_width=0, corner_radius=400)
submit_button.grid(row=2, column=4)
clear_button = customtkinter.CTkButton(button_frame, image=cimage, text="", width=20, height=20, border_width=0, corner_radius=400)
clear_button.configure(command=lambda: clear_output())
clear_button.grid(row=2, column=10) 
help_button = customtkinter.CTkButton(button_frame, image=himage, text="", width=20, height=20, border_width=0, corner_radius=400)
help_button.configure(command=lambda: open_help_window())
help_button.grid(row=2, column=14)
mute_button = customtkinter.CTkButton(button_frame, image=muimage, text="", command=mute, width=20, height=20, border_width=0, corner_radius=400)
mute_button.grid(row=2, column=8)
tools_button= customtkinter.CTkButton(button_frame, image=timage, text="", command=open_Tools_window, width=20, height=20, border_width=0, corner_radius=400 )
tools_button.grid(row=2, column=12)




listen_state = False
root.bind('<Return>', check_input)
root.mainloop()