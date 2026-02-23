import tkinter as tk
from tkinter import messagebox, ttk

# Constants
LIGHT_BACKGROUND = '#ffffff'
LIGHT_ACCENT = '#add8e6'
DARK_TEXT = '#000000'

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tibia Hunt Tracker')
        self.config(bg=LIGHT_BACKGROUND)
        self.geometry('800x600')
        self.iconphoto(False, tk.PhotoImage(file='cockapoo_logo.png')) # Assuming the logo file is present
        self.create_widgets()

    def create_widgets(self):
        self.create_login_frame()
        self.create_hunt_form()
        self.create_hunt_history()
        self.create_statistics_dashboard()
        self.create_cloud_sync_tab()

    def create_login_frame(self):
        self.login_frame = tk.Frame(self, bg=LIGHT_BACKGROUND)
        self.login_frame.pack(pady=20)
        tk.Label(self.login_frame, text='Login', bg=LIGHT_BACKGROUND, font=('Arial', 24), fg=DARK_TEXT).pack()
        tk.Label(self.login_frame, text='Username', bg=LIGHT_BACKGROUND, fg=DARK_TEXT).pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()
        tk.Label(self.login_frame, text='Password', bg=LIGHT_BACKGROUND, fg=DARK_TEXT).pack()
        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.pack()
        tk.Button(self.login_frame, text='Login', command=self.login).pack(pady=10)

    def login(self):
        # Implement login logic here
        messagebox.showinfo('Login', 'Login functionality not implemented.')

    def create_hunt_form(self):
        self.hunt_form_frame = tk.Frame(self, bg=LIGHT_BACKGROUND)
        self.hunt_form_frame.pack(pady=20)
        tk.Label(self.hunt_form_frame, text='New Hunt Form', bg=LIGHT_BACKGROUND, font=('Arial', 24), fg=DARK_TEXT).pack()
        self.hunt_name_entry = self.create_entry('Name')
        self.hunt_level_entry = self.create_entry('Level')
        self.hunt_experience_entry = self.create_entry('Experience')
        self.hunt_duration_entry = self.create_entry('Duration')
        self.hunt_location_entry = self.create_entry('Location')
        tk.Button(self.hunt_form_frame, text='Add Hunt', command=self.add_hunt).pack(pady=10)

    def create_entry(self, label):
        tk.Label(self.hunt_form_frame, text=label, bg=LIGHT_BACKGROUND, fg=DARK_TEXT).pack()
        entry = tk.Entry(self.hunt_form_frame)
        entry.pack()
        return entry

    def add_hunt(self):
        # Implement logic to add a hunt
        messagebox.showinfo('Add Hunt', 'Add Hunt functionality not implemented.')

    def create_hunt_history(self):
        self.history_frame = tk.Frame(self, bg=LIGHT_BACKGROUND)
        self.history_frame.pack(pady=20)
        tk.Label(self.history_frame, text='Hunt History', bg=LIGHT_BACKGROUND, font=('Arial', 24), fg=DARK_TEXT).pack()
        self.hunt_history_tree = ttk.Treeview(self.history_frame)
        self.hunt_history_tree['columns'] = ('Name', 'Level', 'Experience', 'Duration', 'Location', 'Actions')
        for column in self.hunt_history_tree['columns']:
            self.hunt_history_tree.heading(column, text=column)
        self.hunt_history_tree.pack()
        tk.Button(self.history_frame, text='Delete selected', command=self.delete_selected_hunt).pack(pady=10)

    def delete_selected_hunt(self):
        # Implement logic to delete a selected hunt
        messagebox.showinfo('Delete Hunt', 'Delete functionality not implemented.')

    def create_statistics_dashboard(self):
        self.stats_frame = tk.Frame(self, bg=LIGHT_BACKGROUND)
        self.stats_frame.pack(pady=20)
        tk.Label(self.stats_frame, text='Statistics', bg=LIGHT_BACKGROUND, font=('Arial', 24), fg=DARK_TEXT).pack()
        self.stats_text = tk.Text(self.stats_frame, height=10, width=50)
        self.stats_text.pack()

    def create_cloud_sync_tab(self):
        self.sync_frame = tk.Frame(self, bg=LIGHT_BACKGROUND)
        self.sync_frame.pack(pady=20)
        tk.Label(self.sync_frame, text='Cloud Sync', bg=LIGHT_BACKGROUND, font=('Arial', 24), fg=DARK_TEXT).pack()
        tk.Button(self.sync_frame, text='Sync with Railway API', command=self.cloud_sync).pack(pady=10)

    def cloud_sync(self):
        # Implement API sync logic here
        messagebox.showinfo('Cloud Sync', 'Cloud sync functionality not implemented.')

if __name__ == '__main__':
    app = Application()
    app.mainloop()