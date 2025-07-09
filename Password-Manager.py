from tkinter import *
from tkinter import messagebox, ttk, filedialog
import random
import json
from pathlib import Path
import os
import csv
import shutil

root = Tk()
root.geometry("800x550")
root.title("Password Manager")

passstr = StringVar()
passlen = IntVar()
passlen.set(0)
name_str = StringVar()
url_str = StringVar()
username_str = StringVar()

password_levels = ["PIN", "Alphabets & Numbers", "Advanced"]
selected_level = StringVar()
selected_level.set(password_levels[0])

THEMES = {
    "Light": {
        "bg": "#ffffff",
        "fg": "#000000",
        "entry_bg": "#ffffff",
        "entry_fg": "#000000",
        "button_bg": "#f0f0f0",
        "button_fg": "#000000",
        "select_bg": "#cce6ff",
        "select_fg": "#000000"
    },
    "Dark": {
        "bg": "#23272A",
        "fg": "#ffffff",
        "entry_bg": "#2C2F33",
        "entry_fg": "#ffffff",
        "button_bg": "#7289DA",
        "button_fg": "#ffffff",
        "select_bg": "#99aab5",
        "select_fg": "#23272A"
    },
    "Solarized Light": {
        "bg": "#fdf6e3",
        "fg": "#657b83",
        "entry_bg": "#eee8d5",
        "entry_fg": "#586e75",
        "button_bg": "#93a1a1",
        "button_fg": "#073642",
        "select_bg": "#b58900",
        "select_fg": "#fdf6e3"
    },
    "Solarized Dark": {
        "bg": "#002b36",
        "fg": "#93a1a1",
        "entry_bg": "#073642",
        "entry_fg": "#eee8d5",
        "button_bg": "#586e75",
        "button_fg": "#fdf6e3",
        "select_bg": "#268bd2",
        "select_fg": "#002b36"
    },
    "Nord": {
        "bg": "#2e3440",
        "fg": "#d8dee9",
        "entry_bg": "#3b4252",
        "entry_fg": "#eceff4",
        "button_bg": "#5e81ac",
        "button_fg": "#eceff4",
        "select_bg": "#88c0d0",
        "select_fg": "#2e3440"
    },
    "Dracula": {
        "bg": "#282a36",
        "fg": "#f8f8f2",
        "entry_bg": "#44475a",
        "entry_fg": "#f8f8f2",
        "button_bg": "#6272a4",
        "button_fg": "#f8f8f2",
        "select_bg": "#bd93f9",
        "select_fg": "#282a36"
    },
    "Gruvbox Light": {
        "bg": "#fbf1c7",
        "fg": "#3c3836",
        "entry_bg": "#ebdbb2",
        "entry_fg": "#3c3836",
        "button_bg": "#bdae93",
        "button_fg": "#282828",
        "select_bg": "#d79921",
        "select_fg": "#fbf1c7"
    },
    "Gruvbox Dark": {
        "bg": "#282828",
        "fg": "#ebdbb2",
        "entry_bg": "#3c3836",
        "entry_fg": "#ebdbb2",
        "button_bg": "#b16286",
        "button_fg": "#ebdbb2",
        "select_bg": "#d79921",
        "select_fg": "#282828"
    },
    "One Dark": {
        "bg": "#282c34",
        "fg": "#abb2bf",
        "entry_bg": "#21252b",
        "entry_fg": "#abb2bf",
        "button_bg": "#61afef",
        "button_fg": "#282c34",
        "select_bg": "#98c379",
        "select_fg": "#282c34"
    }
}
current_theme = "Light"

# --- Ensure C:/PwManager, config, and data folder exist ---
def ensure_standard_location():
    base_dir = Path("C:/PwManager")
    data_dir = base_dir / "password_manager_data"
    config_file = base_dir / "config.json"
    base_dir.mkdir(exist_ok=True)
    data_dir.mkdir(exist_ok=True)
    if not config_file.exists():
        config = {"storage_folder": str(data_dir)}
        with open(config_file, "w") as f:
            json.dump(config, f, indent=4)
    return data_dir, config_file

# Call this at the very start
ensure_standard_location()

def get_default_config_path():
    return Path("C:/PwManager/config.json")

def load_config():
    config_path = get_default_config_path()
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_config(config):
    config_path = get_default_config_path()
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
    except Exception:
        pass

def get_data_folder():
    config = load_config()
    folder = config.get("storage_folder")
    if folder and os.path.isdir(folder):
        return Path(folder)
    # fallback to standard location
    data_dir = Path("C:/PwManager/password_manager_data")
    data_dir.mkdir(exist_ok=True)
    return data_dir

def set_storage_folder(new_folder):
    config = load_config()
    config["storage_folder"] = str(new_folder)
    save_config(config)

def move_data_folder(old_folder, new_parent_folder):
    old_folder = Path(old_folder)
    new_parent_folder = Path(new_parent_folder)
    new_folder = new_parent_folder / "password_manager_data"
    if new_folder.exists():
        answer = messagebox.askyesno(
            "Replace Folder",
            f"A folder named 'password_manager_data' already exists in the selected location.\n"
            f"Do you want to replace it with your current data? (This will delete the old folder and all its contents.)"
        )
        if not answer:
            return False
        shutil.rmtree(new_folder)
    shutil.move(str(old_folder), str(new_folder))
    return True

def get_data_file():
    return get_data_folder() / "password_dictionary.json"

def apply_theme_to_window(window, theme):
    window.configure(bg=theme["bg"])
    def recursive_configure(widget):
        cls = widget.__class__.__name__
        try:
            if cls in ["Frame", "LabelFrame"]:
                widget.configure(bg=theme["bg"])
            elif cls == "Label":
                widget.configure(bg=theme["bg"], fg=theme["fg"])
            elif cls == "Entry":
                widget.configure(bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["fg"])
            elif cls == "Text":
                widget.configure(bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["fg"])
            elif cls == "Button":
                widget.configure(bg=theme["button_bg"], fg=theme["button_fg"],
                                 activebackground=theme["select_bg"], activeforeground=theme["select_fg"])
            elif cls == "OptionMenu":
                widget.configure(bg=theme["button_bg"], fg=theme["button_fg"])
        except Exception:
            pass
        for child in widget.winfo_children():
            recursive_configure(child)
    recursive_configure(window)
    try:
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=theme["bg"])
        style.configure('TFrame', background=theme["bg"])
        style.configure('TLabel', background=theme["bg"], foreground=theme["fg"])
        style.configure('TButton', background=theme["button_bg"], foreground=theme["button_fg"])
        style.configure('Treeview', background=theme["entry_bg"], fieldbackground=theme["entry_bg"], foreground=theme["entry_fg"])
        style.map('Treeview', background=[('selected', theme["select_bg"])], foreground=[('selected', theme["select_fg"])])
    except Exception:
        pass

def apply_theme(theme_name):
    theme = THEMES[theme_name]
    apply_theme_to_window(root, theme)

def generate():
    length = passlen.get()
    level = selected_level.get()
    if level == "PIN":
        charset = '0123456789'
    elif level == "Alphabets & Numbers":
        charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    else:
        charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?'
    if length <= 0 or not charset:
        passstr.set("")
        return
    password = ''.join(random.choice(charset) for _ in range(length))
    passstr.set(password)

def copytoclipboard():
    root.clipboard_clear()
    root.clipboard_append(passstr.get())

def save_credentials():
    name = name_str.get().strip()
    url = url_str.get().strip()
    username = username_str.get().strip()
    password = passstr.get()
    note = note_text.get("1.0", END).strip()
    if name and username and password:
        config = load_config()
        storage_folder = config.get("storage_folder")
        if not storage_folder:
            folder = filedialog.askdirectory(title="Select Folder for Password Storage")
            if not folder:
                messagebox.showerror("Save Error", "No folder selected. Cannot save.")
                return
            folder = Path(folder) / "password_manager_data"
            folder.mkdir(exist_ok=True)
            set_storage_folder(str(folder))
        file_path = get_data_file()
        file_path.parent.mkdir(exist_ok=True)
        if file_path.exists():
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}
        key = f"{name}|{username}"
        data[key] = {
            "name": name,
            "url": url,
            "username": username,
            "password": password,
            "note": note
        }
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Saved", "Password has been saved successfully.")
        name_str.set("")
        url_str.set("")
        username_str.set("")
        passstr.set("")
        passlen.set(0)
        note_text.delete("1.0", END)
    else:
        messagebox.showerror("Save Error", "Please fill in Name, Username/Email, and Password.")

def import_passwords():
    import_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")],
        title="Import Passwords from CSV"
    )
    if not import_path:
        return
    imported = 0
    try:
        with open(import_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = [row for row in reader]
    except Exception as e:
        messagebox.showerror("Import Error", f"Failed to read CSV file:\n{e}")
        return
    file_path = get_data_file()
    if file_path.exists():
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    for row in rows:
        name = row.get("name", "").strip()
        url = row.get("url", "").strip()
        username = row.get("username", "").strip()
        password = row.get("password", "")
        note = row.get("note", "")
        if name and username and password:
            key = f"{name}|{username}"
            data[key] = {
                "name": name,
                "url": url,
                "username": username,
                "password": password,
                "note": note
            }
            imported += 1
    file_path.parent.mkdir(exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    messagebox.showinfo(
        "Import Complete",
        f"Imported {imported} passwords from:\n{import_path}"
    )

def export_passwords():
    file_path = get_data_file()
    if file_path.exists():
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Export Error", "Password file is corrupted.")
                return
    else:
        messagebox.showinfo("Export Passwords", "No passwords to export.")
        return
    if not data:
        messagebox.showinfo("Export Passwords", "No passwords to export.")
        return
    export_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Export Passwords As"
    )
    if not export_path:
        return
    with open(export_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "url", "username", "password", "note"])
        for entry in data.values():
            writer.writerow([
                entry.get("name", ""),
                entry.get("url", ""),
                entry.get("username", ""),
                entry.get("password", ""),
                entry.get("note", "")
            ])
    messagebox.showinfo("Export Complete", f"Passwords exported successfully to:\n{export_path}")

def change_storage_location():
    old_folder = get_data_folder()
    new_parent_folder = filedialog.askdirectory(title="Select New Parent Folder for password_manager_data")
    if not new_parent_folder:
        return
    new_folder = Path(new_parent_folder) / "password_manager_data"
    if new_folder == old_folder:
        messagebox.showinfo("Storage Location", "Selected folder is already the current storage location.")
        return
    moved = move_data_folder(old_folder, new_parent_folder)
    if moved is False:
        return
    set_storage_folder(str(new_folder))
    messagebox.showinfo("Storage Location", f"Storage location changed to:\n{new_folder}")

def open_manage_passwords():
    manage_win = Toplevel(root)
    manage_win.title("Manage Passwords")
    manage_win.geometry("1000x500")
    columns = ("S. No.", "Name", "URL", "Username/Email", "Password", "Note")
    tree = ttk.Treeview(manage_win, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        if col == "Note":
            tree.column(col, width=200)
        elif col == "Password":
            tree.column(col, width=120)
        elif col == "Username/Email":
            tree.column(col, width=140)
        elif col == "URL":
            tree.column(col, width=180)
        elif col == "Name":
            tree.column(col, width=120)
        elif col == "S. No.":
            tree.column(col, width=40, anchor=CENTER)
        else:
            tree.column(col, width=60, anchor=CENTER)
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    note_display = Text(manage_win, width=80, height=4, wrap=WORD, font=("calibri", 11))
    note_display.pack(fill=X, padx=10, pady=(0,10))
    note_display.config(state=DISABLED)
    file_path = get_data_file()
    if file_path.exists():
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    for i, (key, entry) in enumerate(data.items(), 1):
        name = entry.get("name", "")
        url = entry.get("url", "")
        username = entry.get("username", "")
        pwd = entry.get("password", "")
        note = entry.get("note", "")
        tree.insert("", END, values=(i, name, url, username, pwd, note))
    edit_entry = None
    edit_column = None
    edit_item = None
    def on_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected, 'values')
            note = values[5] if len(values) > 5 else ""
            note_display.config(state=NORMAL)
            note_display.delete("1.0", END)
            note_display.insert(END, note)
            note_display.config(state=DISABLED)
    tree.bind('<<TreeviewSelect>>', on_select)
    def on_double_click(event):
        nonlocal edit_entry, edit_column, edit_item
        if edit_entry:
            edit_entry.destroy()
            edit_entry = None
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = tree.identify_row(event.y)
        column = tree.identify_column(event.x)
        if not row_id or not column:
            return
        if column == '#1':
            return  # S. No. not editable
        x, y, width, height = tree.bbox(row_id, column)
        col_index = int(column.replace('#', '')) - 1
        current_value = tree.item(row_id)['values'][col_index]
        edit_entry = Entry(manage_win)
        edit_entry.place(x=x + tree.winfo_rootx() - manage_win.winfo_rootx(),
                         y=y + tree.winfo_rooty() - manage_win.winfo_rooty(),
                         width=width, height=height)
        edit_entry.insert(0, current_value)
        edit_entry.focus_set()
        edit_column = col_index
        edit_item = row_id
        def save_edit(event=None):
            nonlocal edit_entry, edit_column, edit_item
            new_value = edit_entry.get()
            values = list(tree.item(edit_item)['values'])
            values[edit_column] = new_value
            tree.item(edit_item, values=values)
            edit_entry.destroy()
            if edit_column == 5:
                note_display.config(state=NORMAL)
                note_display.delete("1.0", END)
                note_display.insert(END, new_value)
                note_display.config(state=DISABLED)
            edit_entry = None
            edit_column = None
            edit_item = None
        edit_entry.bind('<Return>', save_edit)
        edit_entry.bind('<FocusOut>', save_edit)
    tree.bind('<Double-1>', on_double_click)
    def save_all_changes():
        all_items = tree.get_children()
        new_data = {}
        for item in all_items:
            vals = tree.item(item)['values']
            if len(vals) >= 6:
                name = vals[1]
                url = vals[2]
                username = vals[3]
                password = vals[4]
                note = vals[5]
                key = f"{name}|{username}"
                new_data[key] = {
                    "name": name,
                    "url": url,
                    "username": username,
                    "password": password,
                    "note": note
                }
        file_path = get_data_file()
        file_path.parent.mkdir(exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(new_data, f, indent=4)
        messagebox.showinfo("Save Changes", "All changes have been saved successfully.")
    save_button = ttk.Button(manage_win, text="Save Changes", command=save_all_changes)
    save_button.pack(pady=5)
    def storage_location_action():
        change_storage_location()
        manage_win.destroy()
    storage_btn = ttk.Button(manage_win, text="Storage Location", command=storage_location_action)
    storage_btn.pack(pady=5)
    apply_theme_to_window(manage_win, THEMES[current_theme])
    manage_win.lift()

notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill='both')

file_tab = Frame(notebook)
notebook.add(file_tab, text='Home')

Label(file_tab, text="The Password Manager", font="calibri 25 bold").pack()
Label(file_tab, text="By Rama", font="calibri 16 bold").pack()

Label(file_tab, text="Name:", font="calibri 12 bold").pack(pady=(10,0))
Entry(file_tab, textvariable=name_str, width=40).pack(pady=(0,5))

Label(file_tab, text="URL (optional):", font="calibri 12 bold").pack(pady=(0,0))
Entry(file_tab, textvariable=url_str, width=40).pack(pady=(0,5))

Label(file_tab, text="Username / Email:", font="calibri 12 bold").pack(pady=(0,0))
Entry(file_tab, textvariable=username_str, width=40).pack(pady=(0,5))

Label(file_tab, text="Note:", font="calibri 12 bold").pack(pady=(0,0))
note_text = Text(file_tab, width=55, height=3, font=("calibri", 11))
note_text.pack(pady=(0,10))

frame_length_type = Frame(file_tab)
frame_length_type.pack(pady=5)
Label(frame_length_type, text="Password Length:", font="calibri 12 bold").grid(row=0, column=0, padx=(0,5))
Entry(frame_length_type, textvariable=passlen, width=5).grid(row=0, column=1, padx=(0,15))
Label(frame_length_type, text="Password Type:", font="calibri 12 bold").grid(row=0, column=2, padx=(0,5))
OptionMenu(frame_length_type, selected_level, *password_levels).grid(row=0, column=3)

frame_password = Frame(file_tab)
frame_password.pack(pady=10)
Label(frame_password, text="Password:", font="calibri 12 bold").grid(row=0, column=0, padx=(0,5))
Entry(frame_password, textvariable=passstr, width=30).grid(row=0, column=1, padx=(0,10))
Button(frame_password, text="Generate Password", command=generate).grid(row=0, column=2)

Button(file_tab, text="Copy to clipboard", command=copytoclipboard).pack(pady=3)
Button(file_tab, text="Save", command=save_credentials).pack(pady=10)

manage_tab = Frame(notebook)
notebook.add(manage_tab, text='Manage Passwords')
Button(manage_tab, text="Open Manage Passwords Window", command=open_manage_passwords).pack(pady=20)

import_export_frame = Frame(manage_tab)
import_export_frame.pack(pady=10)
Button(import_export_frame, text="Import Passwords", command=import_passwords).grid(row=0, column=0, padx=10)
Button(import_export_frame, text="Export Passwords", command=export_passwords).grid(row=0, column=1, padx=10)

appearance_tab = Frame(notebook)
notebook.add(appearance_tab, text='Appearance')
Label(appearance_tab, text="Appearance & Theme", font="calibri 18 bold").pack(pady=(10, 5))
theme_var = StringVar()
theme_var.set(current_theme)
def set_theme():
    global current_theme
    current_theme = theme_var.get()
    apply_theme(current_theme)
    apply_theme_to_window(root, THEMES[current_theme])
Label(appearance_tab, text="Choose Theme:", font="calibri 12 bold").pack(anchor=W, padx=20, pady=(10, 0))
for theme_name in THEMES:
    Radiobutton(appearance_tab, text=theme_name, variable=theme_var, value=theme_name, command=set_theme, font=("calibri", 12)).pack(anchor=W, padx=40)

help_tab = Frame(notebook)
notebook.add(help_tab, text='Help')

help_text = """
How to Use the Password Manager

1. Adding a New Password
- Go to the Home tab.
- Enter the Name (e.g., Google), URL (optional), Username/Email, and (optional) Note.
- Set Password Length and choose Password Type.
- Click Generate Password.
- Click Copy to clipboard if needed.
- Click Save to store the entry.

2. Managing Saved Passwords
- Go to the Manage Passwords tab.
- Click Open Manage Passwords Window to view all entries.
- Double-click any cell (except S. No.) to edit its value.
- Click a row to view the full note below the table.
- Click Save Changes to save all edits.
- Click Storage Location to move your password storage folder.

3. Exporting Passwords
- In the Manage Passwords tab, click Export Passwords.
- Choose where to save the CSV file.

4. Importing Passwords
- In the Manage Passwords tab, click Import Passwords.
- Select a CSV file with columns: name, url, username, password, note.

5. General Tips
- All data is saved in your selected folder.
- You will see an error if required fields are empty.
- A confirmation appears after saving.
"""

Label(help_tab, text="Help & Instructions", font="calibri 18 bold").pack(pady=(10, 5))
help_box = Text(help_tab, wrap=WORD, font=("calibri", 12), width=90, height=20, bg="#f8f8f8")
help_box.pack(padx=10, pady=10, fill=BOTH, expand=True)
help_box.insert(END, help_text)
help_box.config(state=DISABLED)

apply_theme(current_theme)
apply_theme_to_window(root, THEMES[current_theme])
root.mainloop()
