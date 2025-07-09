```markdown
# Password Manager App

A modern, offline password manager built with Python and Tkinter.  
Features include password generation, secure storage, import/export, editable tables, notes, multiple color themes, and a user-selectable storage location.

---

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Getting Started](#getting-started)
- [Usage Instructions](#usage-instructions)
- [Storage Location](#storage-location)
- [Theme Support](#theme-support)
- [Import & Export](#import--export)
- [Data Storage](#data-storage)
- [Dependencies & Imports](#dependencies--imports)
- [Folder Structure](#folder-structure)

---

## Features

- **Tabbed Interface:** Home, Manage Passwords, Appearance, Storage Location, and Help tabs.
- **Password Generation:** Generate strong passwords (PIN, Alphanumeric, Advanced).
- **Credential Management:** Add, edit, and save credentials with name, URL, username/email, password, and note.
- **Editable Table:** Double-click any cell (except S. No.) to edit, then save changes.
- **Import/Export:** Import from and export to CSV files (compatible with browser password exports).
- **Theme Support:** Toggle between Light, Dark, Solarized, Nord, Dracula, Gruvbox, and One Dark themes.
- **User-Selectable Storage Location:** Choose and change where your password data is stored.
- **Help Tab:** Built-in instructions for users.
- **Persistent Storage:** All data saved in a user-selected folder for privacy and portability.

---

## Screenshots

*(Add screenshots here if desired)*

---

## Getting Started

### 1. Clone the Repository

```

git clone https://github.com/yourusername/password-manager.git
cd password-manager

```

### 2. Install Dependencies

Make sure you have Python 3.7+ installed.

Install required packages (if not already present):

```

pip install tk

```

> **Note:** All other libraries (`random`, `json`, `os`, `csv`, `pathlib`, `shutil`) are part of the Python standard library.

### 3. Run the Application

```

python Password-Manager.py

```

---

## Usage Instructions

### Adding a New Password

1. Go to the **Home** tab.
2. Enter the **Name** (e.g., Google), **URL** (optional), **Username/Email**, and (optional) **Note**.
3. Set **Password Length** and select **Password Type**.
4. Click **Generate Password** (or enter your own).
5. Click **Copy to clipboard** if needed.
6. Click **Save** to store the entry.

### Managing Saved Passwords

- Go to the **Manage Passwords** tab.
- Click **Open Manage Passwords Window** to view all entries.
- Double-click any cell (except S. No.) to edit its value.
- Click a row to view the full note below the table.
- Click **Save Changes** to persist your edits.
- Click **Storage Location** to move your password storage folder.

### Exporting Passwords

- In the **Manage Passwords** tab, click **Export Passwords**.
- Choose a location and filename to save all passwords and notes as a CSV file.

### Importing Passwords

- In the **Manage Passwords** tab, click **Import Passwords**.
- Select a CSV file with columns: name, url, username, password, note.
- Imported passwords will be added/merged into your saved entries.

---

## Storage Location

- On first save, you will be prompted to select a folder for storing your password data.
- You can change this location at any time by clicking **Storage Location** in the Manage Passwords window.
- All password data is stored in the selected folder as `password_dictionary.json`.
- The app never creates unnecessary nested folders; your selected folder is the direct home for your data.

---

## Theme Support

- Go to the **Appearance** tab.
- Select from multiple themes: Light, Dark, Solarized Light/Dark, Nord, Dracula, Gruvbox Light/Dark, One Dark.
- The entire interface updates instantly.

---

## Import & Export

- **Export:** Saves all credentials and notes to a CSV file.
- **Import:** Reads a CSV file and merges credentials into your password store.
- CSV columns required: `name`, `url`, `username`, `password`, `note` (compatible with most browser exports).

---

## Data Storage

- All credentials are stored in a file:  
  `<your_selected_folder>/password_dictionary.json`
- The folder is chosen by you (on first save or via Storage Location).
- Data is never sent online and remains fully offline and portable.

---

## Dependencies & Imports

The following Python modules are used:

| Module         | Purpose                                      | Stdlib? |
|----------------|----------------------------------------------|---------|
| tkinter        | GUI framework                                | Yes     |
| ttk            | Themed widgets for Tkinter                   | Yes     |
| messagebox     | System dialogs (info, error, etc.)           | Yes     |
| filedialog     | Open/Save dialogs                            | Yes     |
| random         | Password generation                          | Yes     |
| json           | Data storage                                 | Yes     |
| pathlib        | File/folder path management                  | Yes     |
| os             | OS path utilities                            | Yes     |
| csv            | Import/export CSV files                      | Yes     |
| shutil         | Folder/file moving and copying               | Yes     |

---

## Folder Structure

```

password-manager/
├── Password-Manager.py
├── <your_selected_folder>/
│   └── password_dictionary.json
└── README.md

```

## Notes

- All data is stored **locally** and is never uploaded or shared.
- For best security, regularly export your passwords as a backup.
- If you encounter issues, please open an issue on GitHub or contact the maintainer.

---
```

