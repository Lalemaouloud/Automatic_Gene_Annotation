from tkinter import Tk, Frame, Label, Text, Button, filedialog, Canvas
from PIL import ImageTk, Image
import webbrowser
import os
from src.script import main
from tkinter import *
from PIL import Image


class Interface:
    def __init__(self):
        self.window = Tk()
        self.window.title("Gene Automated Annotation Table")
        self.window.geometry("800x850")

        # Set up canvas as the main container (to add a background image)
        self.canvas = Canvas(self.window, width=1500, height=850)
        self.canvas.pack()

        # Set up frames to organize the widgets
        self.header_frame = Frame(self.canvas, bg="#590c0c", width=800, height=200)
        self.content_frame = Frame(self.canvas,bg="#590c0c", width=800, height=350)
        self.button_frame = Frame(self.canvas, bg="#590c0c", width=800, height=150)
        self.footer_frame = Frame(self.canvas, bg="#264653", width=800, height=150)

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        self.create_header()
        self.create_content()
        self.create_buttons()
        self.create_footer()

    def create_header(self):
        self.title_label = Label(self.header_frame,
                                 text="Gene Automated Annotation Table",
                                 font=("Geneva", 26, "italic"),
                                 fg="#eef527",
                                 bg="#590c0c")
        self.title_label.pack(pady=25)

        self.img = Image.open('img/Cloud5.jpg')
        self.database_img = ImageTk.PhotoImage(self.img.resize((289, 170)))
        database_label = Label(self.header_frame, image=self.database_img)
        database_label.pack(pady=25)

        self.header_frame.pack(fill="x")

    def create_content(self):
        label_title = Label(self.content_frame,
                            text="Initial Data",
                            font=("Geneva", 26, "italic"),
                            fg="#eef527",
                            bg="#590c0c")
        label_title.pack(pady=15)

        self.txt = Text(self.content_frame, height=10, width=60,
                        wrap="word",
                        fg="#264653",
                        bg="white",
                        font=("Arial", 14))
        self.txt.insert('1.0', 'Insert your data here or select a file with the button below. It should be a .txt file, in the format "gene organism"')
        self.txt.pack(pady=12)

        self.content_frame.pack(fill="x", pady=20)

    def create_buttons(self):
        button_import = Button(self.button_frame,
                               text='Insert File',
                               command=self.import_file,
                               bg="#2A9D8F",
                               font=("Arial", 14))
        button_import.pack(fill="x", padx=20, pady=5)

        button_upload = Button(self.button_frame,
                               text='Execute',
                               command=self.execute,
                               bg="#2A9D8F",
                               font=("Arial", 14))
        button_upload.pack(fill="x", padx=20, pady=5)

        button_open = Button(self.button_frame,
                             text='Open Results',
                             command=self.open_file,
                             bg="#2A9D8F",
                             font=("Arial", 14))
        button_open.pack(fill="x", padx=20, pady=5)

        self.button_frame.pack(fill="x", pady=20)

    def create_footer(self):
        foot_text = Label(self.footer_frame,
                          text="MAOULOUD Lale | CARON Mathias | LOUIS Mael\nMASTER 1 BIMS\nUniversity of Rouen-Normandy\n2023-2024",
                          font=("Arial", 10, "italic"),
                          bg="#264653",
                          fg="#F4A261")
        foot_text.pack(pady=10)

        self.footer_frame.pack(fill="x", side="bottom")






    def import_file(self):
        global filename
        filename = filedialog.askopenfilename(filetypes=(
            ("TXT files", "*.txt"), ("All files", "*.*")))
        openedFile = open(filename)
        readFile = openedFile.read()
        self.txt.delete(1.0, END)
        self.txt.insert('1.0', readFile)

    def execute(self):
        main(filename, self.txt)

    def open_file(self):   
        webbrowser.open('file://' + os.path.realpath('Results.html'))
        

    def set_title(self, new_title):
        self.title_label.config(text=new_title)

    def set_background_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize((800, 850), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor='nw', image=photo)
        self.canvas.image = photo  

