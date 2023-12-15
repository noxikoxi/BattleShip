import tkinter as tk
from tkinter import ttk  # themed widgets


class Popup:
    def __init__(self):
        self.root = tk.Tk()
        WIDTH, HEIGHT = 500, 300
        self.root.resizable(False, False)
        self.root.geometry(f'{WIDTH}x{HEIGHT}')
        self.root.title('Battleships')

        nameLabel = ttk.Label(self.root, text="Your name:", font='Times 18', padding=10)
        nameLabel.pack()

        self.name = tk.Entry(self.root)
        self.name.pack()

        ipLabel = ttk.Label(self.root, text="Server IP:", font='Times 18', padding=10)
        ipLabel.pack()

        self.ip = ttk.Entry(self.root)
        self.ip.pack()

        space = ttk.Label(self.root, text="", font='Times 18', padding=10)
        space.pack()

        self.playBtn = ttk.Button(self.root, text="PLAY", padding=10)
        self.playBtn.pack()

    def updateButtonCommand(self, func):
        self.playBtn['command'] = func

    def run(self):
        self.root.mainloop()
