# Password Manager App

A modern, user-friendly offline password manager built with Python and Tkinter.  
Features include password generation, secure storage, import/export, editable tables, notes, and Light/Dark theme support.

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Usage Instructions](#usage-instructions)
- [Theme Support](#theme-support)
- [Data Storage](#data-storage)
- [Import & Export](#import--export)
- [Dependencies & Imports](#dependencies--imports)
- [Folder Structure](#folder-structure)
- [License](#license)

---

## Features

- **Tabbed Interface:** Home, Manage Passwords, Appearance, and Help tabs.
- **Password Generation:** Generate strong passwords (PIN, Alphanumeric, Advanced).
- **Credential Management:** Add, edit, and save credentials with notes.
- **Editable Table:** Double-click any cell (except S. No.) to edit, then save changes.
- **Import/Export:** Import from and export to CSV files.
- **Theme Support:** Toggle between Light and Dark themes.
- **Help Tab:** Built-in instructions for users.
- **Persistent Storage:** All data saved in a local JSON file for privacy and portability.

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

> **Note:** All other libraries (`random`, `json`, `os`, `csv`, `pathlib`) are part of the Python standard library.

### 3. Run the Application

```

python Password-Generator.py

```

---

## Usage Instructions

### Adding a New Password

1. Go to the **Home** tab.
2. Enter your **Username / Email**.
3. (Optional) Enter a **Note**.
4. Set **Password Length** and select **Password Type**.
5. Click **Generate Password** (or enter your own).
6. Click **Copy to clipboard** if needed.
7. Click **Save** to store the entry.

### Managing Saved Passwords

- Go to the **Manage Passwords** tab.
- Click **Open Manage Passwords Window** to view all entries.
- Double-click any cell (except S. No.) to edit its value.
- Click a row to view the full note below the table.
- Click **Save Changes** to persist your edits.

### Exporting Passwords

- In the **Home** or **Manage Passwords** tab, click **Export Passwords**.
- Choose a location and filename to save all passwords and notes as a CSV file.

### Importing Passwords

- In the **Home** or **Manage Passwords** tab, click **Import Passwords**.
- Select a CSV file with columns: Username/Email, Password, and Note.
- Imported passwords will be added/merged into your saved entries.

---

## Theme Support

- Go to the **Appearance** tab.
- Select **Light** or **Dark** theme using the radio buttons.
- The entire interface updates instantly.

---

## Data Storage

- All credentials are stored in a file:  
  `password_manager_data/password_dictionary.json`
- This folder and file are created in the same directory as the script.
- Data is never sent online and remains fully offline and portable.

---

## Import & Export

- **Export:** Saves all credentials and notes to a CSV file.
- **Import:** Reads a CSV file and merges credentials into your password store.
- CSV columns required: `Username/Email`, `Password`, `Note`.

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

---

## Folder Structure

```

password-manager/
├── Password-Generator.py
├── password_manager_data/
│   └── password_dictionary.json
└── README.md

```

---

## License

This project is open-source and free to use under the MIT License.

---

## Notes

- All data is stored **locally** and is never uploaded or shared.
- For best security, regularly export your passwords as a backup.
- If you encounter issues, please open an issue on GitHub or contact the maintainer.

---