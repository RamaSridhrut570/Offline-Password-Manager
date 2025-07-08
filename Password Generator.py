from tkinter import *
from tkinter import messagebox, ttk, filedialog
import random
import json
from pathlib import Path
import os
import csv

root = Tk()
root.geometry("800x500")
root.title("Password Manager")

passstr = StringVar()
passlen = IntVar()
passlen.set(0)
username_str = StringVar()

password_levels = ["PIN", "Alphabets & Numbers", "Advanced"]
selected_level = StringVar()
selected_level.set(password_levels[0])

# Theme definitions
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
    }
}
current_theme = "Light"

# Always use the script's directory for data storage
script_dir = Path(os.path.abspath(os.path.dirname(__file__)))
data_folder = script_dir / 'password_manager_data'
file_path = data_folder / 'password_dictionary.json'

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
    username = username_str.get().strip()
    password = passstr.get()
    note = note_text.get("1.0", END).strip()
    if username and password:
        data_folder.mkdir(exist_ok=True)
        if file_path.exists():
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}
        data[username] = {"password": password, "note": note}
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Saved", "Password has been saved successfully.")
        username_str.set("")
        passstr.set("")
        passlen.set(0)
        note_text.delete("1.0", END)
    else:
        messagebox.showerror("Save Error", "Fields are empty, Nothing to save.")

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
    if file_path.exists():
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    for row in rows:
        user = row.get("Username/Email", "").strip()
        pwd = row.get("Password", "")
        note = row.get("Note", "")
        if user and pwd:
            data[user] = {"password": pwd, "note": note}
            imported += 1
    data_folder.mkdir(exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    messagebox.showinfo(
        "Import Complete",
        f"Imported {imported} passwords from:\n{import_path}"
    )

def export_passwords():
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
        writer.writerow(["Username/Email", "Password", "Note"])
        for user, entry in data.items():
            if isinstance(entry, dict):
                pwd = entry.get("password", "")
                note = entry.get("note", "")
            else:
                pwd = entry
                note = ""
            writer.writerow([user, pwd, note])
    messagebox.showinfo("Export Complete", f"Passwords exported successfully to:\n{export_path}")

def open_manage_passwords():
    manage_win = Toplevel(root)
    manage_win.title("Manage Passwords")
    manage_win.geometry("700x500")
    columns = ("S. No.", "Username/Email", "Password", "Note")
    tree = ttk.Treeview(manage_win, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        if col == "Note":
            tree.column(col, width=260)
        elif col == "Password":
            tree.column(col, width=140)
        elif col == "Username/Email":
            tree.column(col, width=180)
        elif col == "S. No.":
            tree.column(col, width=40, anchor=CENTER)
        else:
            tree.column(col, width=60, anchor=CENTER)
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    note_display = Text(manage_win, width=80, height=4, wrap=WORD, font=("calibri", 11))
    note_display.pack(fill=X, padx=10, pady=(0,10))
    note_display.config(state=DISABLED)
    if file_path.exists():
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    for i, (user, entry) in enumerate(data.items(), 1):
        if isinstance(entry, dict):
            pwd = entry.get("password", "")
            note = entry.get("note", "")
        else:
            pwd = entry
            note = ""
        tree.insert("", END, values=(i, user, pwd, note))
    edit_entry = None
    edit_column = None
    edit_item = None
    def on_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected, 'values')
            note = values[3] if len(values) > 3 else ""
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
            if edit_column == 3:
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
            if len(vals) >= 4:
                username = vals[1]
                password = vals[2]
                note = vals[3]
                new_data[username] = {"password": password, "note": note}
        data_folder.mkdir(exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(new_data, f, indent=4)
        messagebox.showinfo("Save Changes", "All changes have been saved successfully.")
    save_button = ttk.Button(manage_win, text="Save Changes", command=save_all_changes)
    save_button.pack(pady=5)
    apply_theme_to_window(manage_win, THEMES[current_theme])
    manage_win.lift()

notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill='both')

file_tab = Frame(notebook)
notebook.add(file_tab, text='Home')

Label(file_tab, text="The Password Manager", font="calibri 25 bold").pack()
Label(file_tab, text="By Rama", font="calibri 16 bold").pack()

Label(file_tab, text="Username / Email:", font="calibri 12 bold").pack(pady=(10,0))
Entry(file_tab, textvariable=username_str, width=40).pack(pady=(0,10))

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
Radiobutton(appearance_tab, text="Light", variable=theme_var, value="Light", command=set_theme, font=("calibri", 12)).pack(anchor=W, padx=40)
Radiobutton(appearance_tab, text="Dark", variable=theme_var, value="Dark", command=set_theme, font=("calibri", 12)).pack(anchor=W, padx=40)

help_tab = Frame(notebook)
notebook.add(help_tab, text='Help')

help_text = """
How to Use the Password Manager

1. Adding a New Password
- Go to the Home tab.
- Enter your Username / Email.
- (Optional) Enter a Note.
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

3. Exporting Passwords
- In the Home tab, click Export Passwords.
- Choose where to save the CSV file.

4. Importing Passwords
- In the Home tab, click Import Passwords.
- Select a CSV file with Username/Email, Password, and Note columns.

5. General Tips
- All data is saved in the password_manager_data folder in the app directory.
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
