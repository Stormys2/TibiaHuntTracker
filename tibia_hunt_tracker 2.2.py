import tkinter as tk
from tkinter import ttk
import emoji

class TibiaHuntTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Tibia Hunt Tracker")
        self.root.geometry('400x300')
        self.root.configure(bg='white')

        # Light Theme
        style = ttk.Style()
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white', foreground='black')
        style.configure('TButton', background='lightblue', padding=5)

        # Logo with emoji
        self.logo = emoji.emojize(':dog:', use_aliases=True)  # Brown cockapoo
        self.title_label = ttk.Label(self.root, text=f'{self.logo} Tibia Hunt Tracker', font=('Helvetica', 16))
        self.title_label.pack(pady=10)

        # Example button for tracking
        self.track_button = ttk.Button(self.root, text='Start Tracking', command=self.start_tracking)
        self.track_button.pack(pady=20)

    def start_tracking(self):
        print('Tracking started!')

if __name__ == '__main__':
    root = tk.Tk()
    app = TibiaHuntTracker(root)
    root.mainloop()