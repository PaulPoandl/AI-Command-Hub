import customtkinter
import tkinter
import tkinter as tk
from tkinter import ttk, PhotoImage, Entry, Label, Tk, Button
from PIL import Image
import os
import subprocess

Tools = customtkinter.CTk()
Tools.after(300, lambda :Tools.iconbitmap('ICO Icons/AI-Command-Hub Tools.ico'))
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
Tools.title("Tools and AIs")
Tools.geometry("177x60")
Tools.resizable(False, False)

def open_openAI():
    os.startfile("OpenAI Chat.py")
def open_wolframalpha():
    os.startfile("WolframAlpha Chat.py")
def open_translator():
    os.startfile("Translator.py")
def open_calculator():
    calculator_path = r'C:\Windows\System32\calc.exe'
    subprocess.Popen(calculator_path)
def open_explorer():
    subprocess.Popen(['explorer.exe'])
def open_calender():
    try:
        subprocess.run(['start', 'outlookcal:'], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
def open_text_editor():
    notepad_path = r'C:\Windows\System32\notepad.exe'
    subprocess.Popen(notepad_path)
def open_paint():
    subprocess.Popen("mspaint.exe")

command_label1 = customtkinter.CTkLabel(Tools, text=" ")
command_label1.grid(row=1, column=1, padx=2)
command_label5 = customtkinter.CTkLabel(Tools, text=" ")
command_label5.grid(row=2, column=1, padx=2)



wimage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Wolfram Button.png"),
                                dark_image=Image.open("PNG Buttons/Wolfram Button.png"),
                                size=(15, 15))
oimage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/OpenAI Button.png"),
                                dark_image=Image.open("PNG Buttons/OpenAI Button.png"),
                                size=(15, 15))
eimage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Explorer Button.png"),
                                dark_image=Image.open("PNG Buttons/Explorer Button.png"),
                                size=(15, 15))
cimage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Calendar Button.png"),
                                dark_image=Image.open("PNG Buttons/Calendar Button.png"),
                                size=(15, 15))
rimage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Calculator Button.png"),
                                dark_image=Image.open("PNG Buttons/Calculator Button.png"),
                                size=(15, 15))
pimage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Paint Button.png"),
                                dark_image=Image.open("PNG Buttons/Paint Button.png"),
                                size=(15, 15))
nimage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Notepad Button.png"),
                                dark_image=Image.open("PNG Buttons/Notepad Button.png"),
                                size=(15, 15))
timage = customtkinter.CTkImage(light_image=Image.open("PNG Buttons/Translator Button.png"),
                                dark_image=Image.open("PNG Buttons/Translator Button.png"),
                                size=(15, 15))

OpenAI_button = customtkinter.CTkButton(Tools, image=oimage, command=open_openAI, text="", width=20, height=20, border_width=0, corner_radius=400)
OpenAI_button.grid(row=1, column=2, padx=1, pady=2)
Wolframalpha_button = customtkinter.CTkButton(Tools, image=wimage, command=open_wolframalpha, text="", width=20, height=20, border_width=0, corner_radius=400)
Wolframalpha_button.grid(row=1, column=4, padx=1, pady=2)
Explorer_button = customtkinter.CTkButton(Tools, image=eimage, command=open_explorer, text="", width=20, height=20, border_width=0, corner_radius=400)
Explorer_button.grid(row=1, column=6, padx=1, pady=2)
Calendar_button = customtkinter.CTkButton(Tools, image=cimage, command=open_calender, text="", width=20, height=20, border_width=0, corner_radius=400)
Calendar_button.grid(row=1, column=8, padx=1, pady=2)
Calculator_button = customtkinter.CTkButton(Tools, image=rimage, command=open_calculator, text="", width=20, height=20, border_width=0, corner_radius=400)
Calculator_button.grid(row=2, column=2, padx=1, pady=2)
Paint_button = customtkinter.CTkButton(Tools, image=pimage, command=open_paint, text="", width=20, height=20, border_width=0, corner_radius=400)
Paint_button.grid(row=2, column=4, padx=1, pady=2)
Notepad_button = customtkinter.CTkButton(Tools, image=nimage, command=open_text_editor, text="", width=20, height=20, border_width=0, corner_radius=400)
Notepad_button.grid(row=2, column=6, padx=1, pady=2)
Translator_button = customtkinter.CTkButton(Tools, image=timage, command=open_translator, text="", width=20, height=20, border_width=0, corner_radius=400)
Translator_button.grid(row=2, column=8, padx=1, pady=2)

Tools.mainloop()








