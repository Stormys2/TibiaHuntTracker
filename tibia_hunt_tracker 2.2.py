import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
import requests
from pathlib import Path
import threading

# ==================== CONFIGURATION ====================
RAILWAY_API_URL = 'https://tibiahunttracker.up.railway.app/'
LOCAL_DATA_FILE = 'hunts_data.json'
jwt_token = None

# ==================== API FUNCTIONS ====================
def api_request(endpoint, method='GET', data=None):
    """Make API requests with JWT authentication"""
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json'
    }
    url = f'{RAILWAY_API_URL}{endpoint}'
    try:
        response = requests.request(method, url, json=data, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json(), True
        else:
            return response.text, False
    except Exception as e:
        return str(e), False

def register(username, password):
    """Register a new user"""
    data = {'username': username, 'password': password}
    return api_request('auth/register', 'POST', data)

def login(username, password):
    """Login and retrieve JWT token"""
    global jwt_token
    data = {'username': username, 'password': password}
    result, success = api_request('auth/login', 'POST', data)
    if success and 'token' in result:
        jwt_token = result['token']
    return result, success

def fetch_hunts():
    """Fetch all hunts from the cloud"""
    if not jwt_token:
        return [], False
    return api_request('hunts', 'GET')

def save_hunt(hunt_data):
    """Save a hunt to the cloud"""
    if not jwt_token:
        return None, False
    return api_request('hunts', 'POST', hunt_data)

def delete_hunt(hunt_id):
    """Delete a hunt from the cloud"""
    if not jwt_token:
        return None, False
    return api_request(f'hunts/{hunt_id}', 'DELETE')

# ==================== LOCAL STORAGE FUNCTIONS ====================
def load_local_hunts():
    """Load hunts from local JSON file"""
    if os.path.exists(LOCAL_DATA_FILE):
        try:
            with open(LOCAL_DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_local_hunts(hunts):
    """Save hunts to local JSON file"""
    try:
        with open(LOCAL_DATA_FILE, 'w') as f:
            json.dump(hunts, f, indent=2)
        return True
    except:
        return False

# ==================== HUNT LOGIC ====================
class HuntTracker:
    def __init__(self):
        self.hunts = load_local_hunts()
        self.next_id = max([h.get('id', 0) for h in self.hunts], default=0) + 1
    
    def create_hunt(self, name, level, exp_gained, time_minutes, location=''):
        """Create a new hunt entry"""
        hunt = {
            'id': self.next_id,
            'name': name,
            'level': level,
            'exp_gained': exp_gained,
            'time_minutes': time_minutes,
            'location': location,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'exp_per_hour': (exp_gained / time_minutes * 60) if time_minutes > 0 else 0,
            'efficiency': self.calculate_efficiency(exp_gained, time_minutes, level)
        }
        self.hunts.append(hunt)
        self.next_id += 1
        save_local_hunts(self.hunts)
        return hunt
    
    def calculate_efficiency(self, exp_gained, time_minutes, level):
        """Calculate hunt efficiency based on level"""
        if time_minutes == 0:
            return 0
        exp_per_hour = (exp_gained / time_minutes) * 60
        # Efficiency based on level and exp/h
        efficiency = (exp_per_hour / (level * 100)) * 100
        return round(efficiency, 2)
    
    def get_stats(self):
        """Get statistics from all hunts"""
        if not self.hunts:
            return {}
        
        total_exp = sum(h['exp_gained'] for h in self.hunts)
        total_time = sum(h['time_minutes'] for h in self.hunts)
        avg_level = sum(h['level'] for h in self.hunts) / len(self.hunts)
        avg_efficiency = sum(h['efficiency'] for h in self.hunts) / len(self.hunts)
        avg_exp_hour = (total_exp / total_time * 60) if total_time > 0 else 0
        
        return {
            'total_hunts': len(self.hunts),
            'total_exp': int(total_exp),
            'total_hours': round(total_time / 60, 2),
            'avg_level': round(avg_level, 1),
            'avg_efficiency': round(avg_efficiency, 2),
            'avg_exp_per_hour': int(avg_exp_hour)
        }
    
    def delete_hunt(self, hunt_id):
        """Delete a hunt by ID"""
        self.hunts = [h for h in self.hunts if h['id'] != hunt_id]
        save_local_hunts(self.hunts)
    
    def sync_with_cloud(self):
        """Sync hunts with cloud"""
        for hunt in self.hunts:
            if 'cloud_synced' not in hunt:
                result, success = save_hunt(hunt)
                if success:
                    hunt['cloud_synced'] = True
        save_local_hunts(self.hunts)

# ==================== GUI APPLICATION ====================
class TibiaHuntTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tibia Hunt Tracker v2.2")
        self.root.geometry("900x700")
        self.root.configure(bg='#2b2b2b')
        
        self.tracker = HuntTracker()
        self.logged_in = False
        self.current_user = None
        
        self.setup_styles()
        self.show_login_screen()
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_color = '#2b2b2b'
        fg_color = '#ffffff'
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TButton', background='#404040', foreground=fg_color)
        style.configure('TEntry', fieldbackground='#404040', foreground=fg_color)
        style.configure('Treeview', background='#3c3c3c', foreground=fg_color, fieldbackground='#3c3c3c')
        style.configure('Treeview.Heading', background='#404040', foreground=fg_color)
    
    def show_login_screen(self):
        """Show login/register screen"""
        self.clear_window()
        
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title = ttk.Label(frame, text="Tibia Hunt Tracker", font=('Arial', 24, 'bold'))
        title.pack(pady=20)
        
        subtitle = ttk.Label(frame, text="Track your hunts and analyze efficiency", font=('Arial', 10))
        subtitle.pack(pady=5)
        
        # Username
        ttk.Label(frame, text="Username:").pack(pady=(20, 5))
        username_entry = ttk.Entry(frame, width=30)
        username_entry.pack()
        
        # Password
        ttk.Label(frame, text="Password:").pack(pady=(15, 5))
        password_entry = ttk.Entry(frame, width=30, show='*')
        password_entry.pack()
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=30)
        
        def login_action():
            username = username_entry.get()
            password = password_entry.get()
            if not username or not password:
                messagebox.showerror("Error", "Username and password required")
                return
            
            result, success = login(username, password)
            if success:
                self.logged_in = True
                self.current_user = username
                messagebox.showinfo("Success", f"Welcome {username}!")
                self.show_main_screen()
            else:
                messagebox.showerror("Login Failed", str(result))
        
        def register_action():
            username = username_entry.get()
            password = password_entry.get()
            if not username or not password:
                messagebox.showerror("Error", "Username and password required")
                return
            
            result, success = register(username, password)
            if success:
                messagebox.showinfo("Success", "Account created! Please login")
            else:
                messagebox.showerror("Registration Failed", str(result))
        
        ttk.Button(button_frame, text="Login", command=login_action, width=15).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Register", command=register_action, width=15).pack(side='left', padx=5)
        
        # Offline mode
        ttk.Button(self.root, text="Continue Offline", command=self.show_main_screen).pack(side='bottom', pady=10)
    
    def show_main_screen(self):
        """Show main application screen"""
        self.clear_window()
        
        # Top bar with user info
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        status_text = f"User: {self.current_user}" if self.current_user else "Offline Mode"
        ttk.Label(top_frame, text=status_text, font=('Arial', 10)).pack(side='left')
        ttk.Button(top_frame, text="Logout", command=self.show_login_screen).pack(side='right')
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: New Hunt
        self.create_hunt_tab(notebook)
        
        # Tab 2: Hunt History
        self.hunt_history_tab(notebook)
        
        # Tab 3: Statistics
        self.statistics_tab(notebook)
        
        # Tab 4: Sync
        self.sync_tab(notebook)
    
    def create_hunt_tab(self, notebook):
        """Create 'New Hunt' tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="New Hunt")
        
        # Form fields
        fields_frame = ttk.Frame(frame)
        fields_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        ttk.Label(fields_frame, text="Hunt Name:").pack(anchor='w', pady=(10, 2))
        name_entry = ttk.Entry(fields_frame, width=40)
        name_entry.pack(anchor='w', pady=(0, 15))
        
        ttk.Label(fields_frame, text="Level:").pack(anchor='w', pady=(10, 2))
        level_entry = ttk.Entry(fields_frame, width=40)
        level_entry.pack(anchor='w', pady=(0, 15))
        
        ttk.Label(fields_frame, text="Experience Gained:").pack(anchor='w', pady=(10, 2))
        exp_entry = ttk.Entry(fields_frame, width=40)
        exp_entry.pack(anchor='w', pady=(0, 15))
        
        ttk.Label(fields_frame, text="Duration (minutes):").pack(anchor='w', pady=(10, 2))
        time_entry = ttk.Entry(fields_frame, width=40)
        time_entry.pack(anchor='w', pady=(0, 15))
        
        ttk.Label(fields_frame, text="Location:").pack(anchor='w', pady=(10, 2))
        location_entry = ttk.Entry(fields_frame, width=40)
        location_entry.pack(anchor='w', pady=(0, 15))
        
        def save_hunt():
            try:
                name = name_entry.get()
                level = int(level_entry.get())
                exp = int(exp_entry.get())
                time = int(time_entry.get())
                location = location_entry.get() or "Unknown"
                
                if not name:
                    messagebox.showerror("Error", "Hunt name required")
                    return
                
                hunt = self.tracker.create_hunt(name, level, exp, time, location)
                messagebox.showinfo("Success", f"Hunt '{name}' saved!")
                
                # Clear fields
                name_entry.delete(0, 'end')
                level_entry.delete(0, 'end')
                exp_entry.delete(0, 'end')
                time_entry.delete(0, 'end')
                location_entry.delete(0, 'end')
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
        
        ttk.Button(fields_frame, text="Save Hunt", command=save_hunt).pack(pady=20)
    
    def hunt_history_tab(self, notebook):
        """Create 'Hunt History' tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Hunt History")
        
        # Treeview
        columns = ('ID', 'Name', 'Level', 'Exp/h', 'Duration', 'Location', 'Date')
        tree = ttk.Treeview(frame, columns=columns, height=15)
        tree.column('#0', width=0, stretch='no')
        tree.column('ID', anchor='center', width=30)
        tree.column('Name', anchor='w', width=120)
        tree.column('Level', anchor='center', width=50)
        tree.column('Exp/h', anchor='center', width=80)
        tree.column('Duration', anchor='center', width=70)
        tree.column('Location', anchor='w', width=100)
        tree.column('Date', anchor='center', width=130)
        
        tree.heading('#0', text='', anchor='w')
        for col in columns:
            tree.heading(col, text=col, anchor='w')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y')
        
        # Refresh hunt list
        def refresh_hunts():
            tree.delete(*tree.get_children())
            for hunt in sorted(self.tracker.hunts, key=lambda x: x['date'], reverse=True):
                tree.insert('', 'end', values=(
                    hunt['id'],
                    hunt['name'],
                    hunt['level'],
                    f"{hunt['exp_per_hour']:.0f}",
                    f"{hunt['time_minutes']}min",
                    hunt['location'],
                    hunt['date']
                ))
        
        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Select a hunt to delete")
                return
            
            item = tree.item(selected[0])
            hunt_id = int(item['values'][0])
            
            if messagebox.askyesno("Confirm", "Delete this hunt?"):
                self.tracker.delete_hunt(hunt_id)
                refresh_hunts()
        
        refresh_hunts()
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Refresh", command=refresh_hunts).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete", command=delete_selected).pack(side='left', padx=5)
    
    def statistics_tab(self, notebook):
        """Create 'Statistics' tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Statistics")
        
        stats_frame = ttk.Frame(frame)
        stats_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        def refresh_stats():
            # Clear previous stats
            for widget in stats_frame.winfo_children():
                widget.destroy()
            
            stats = self.tracker.get_stats()
            
            if not stats:
                ttk.Label(stats_frame, text="No hunts recorded yet", font=('Arial', 12)).pack(pady=20)
                return
            
            # Display stats
            stat_items = [
                ('Total Hunts', stats['total_hunts']),
                ('Total Experience', f"{stats['total_exp']:,}"),
                ('Total Hours', stats['total_hours']),
                ('Average Level', stats['avg_level']),
                ('Average Efficiency', f"{stats['avg_efficiency']}%"),
                ('Average Exp/Hour', f"{stats['avg_exp_per_hour']:,}")
            ]
            
            for label, value in stat_items:
                row_frame = ttk.Frame(stats_frame)
                row_frame.pack(fill='x', pady=10)
                
                ttk.Label(row_frame, text=f"{label}:", font=('Arial', 12, 'bold'), width=20).pack(side='left')
                ttk.Label(row_frame, text=str(value), font=('Arial', 14), foreground='#00ff00').pack(side='left')
        
        refresh_stats()
        
        ttk.Button(frame, text="Refresh Stats", command=refresh_stats).pack(pady=20)
    
    def sync_tab(self, notebook):
        """Create 'Sync' tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Cloud Sync")
        
        info_frame = ttk.Frame(frame)
        info_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        status_label = ttk.Label(info_frame, text="", font=('Arial', 11))
        status_label.pack(pady=20)
        
        def sync_hunts():
            if not self.logged_in:
                messagebox.showwarning("Warning", "Please login to sync with cloud")
                return
            
            status_label.config(text="Syncing...")
            
            def sync_thread():
                try:
                    self.tracker.sync_with_cloud()
                    status_label.config(text="✓ Sync completed successfully!", foreground='#00ff00')
                    messagebox.showinfo("Success", "Hunts synced to cloud!")
                except Exception as e:
                    status_label.config(text=f"✗ Sync failed: {str(e)}", foreground='#ff0000')
            
            threading.Thread(target=sync_thread, daemon=True).start()
        
        ttk.Button(info_frame, text="Sync to Cloud", command=sync_hunts, width=30).pack(pady=10)
        ttk.Label(info_frame, text="Local hunts will be synchronized with your cloud account.").pack(pady=10)
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()

# ==================== MAIN ====================
if __name__ == '__main__':
    root = tk.Tk()
    app = TibiaHuntTrackerApp(root)
    root.mainloop()