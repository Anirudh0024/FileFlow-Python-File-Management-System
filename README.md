# 📁 FileFlow — Python File Management System

FileFlow is a simple and interactive file management web application built using **Python and Streamlit**. It allows users to manage files through a clean web interface without needing to perform file operations manually in the terminal.

## ✨ Features

- **Create Files:** Create new files and add initial content.
- **Read Files:** View the contents of existing files.
- **Update Files:** Overwrite existing content or append new content.
- **Rename Files:** Change the names of existing files.
- **Delete Files:** Delete files with a confirmation step.
- **File Explorer:** View files and folders inside the workspace.
- **Dashboard:** View the total number of files, folders, and file size.
- **Path Validation:** Restrict file operations to the designated workspace.
- **Error Handling:** Display helpful error messages when an operation fails.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pathlib
- Datetime

## 📂 Project Structure

```text
python-fileflow-manager/
├── app.py
├── README.md
├── .gitignore
└── managed_files/
```

The `managed_files` directory is created automatically when the application starts.

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/python-fileflow-manager.git
cd python-fileflow-manager
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
python -m pip install streamlit
```

### 5. Run the Application

```bash
python -m streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser if the application does not open automatically.

## 🚀 How to Use

1. Launch the application.
2. Select an operation from the sidebar.
3. Create a new file or select an existing file.
4. Read, update, rename, or delete files.
5. Visit the Dashboard to view workspace statistics.

## 🔒 Safety and Limitations

- File operations are restricted to the `managed_files` workspace.
- Deleting files requires confirmation.
- The application is primarily designed for text files.
- Files are stored locally on the computer running the application.
- Authentication and multi-user access control are not currently implemented.

## 🎯 Learning Outcomes

This project demonstrates practical knowledge of:

- Python functions, loops, conditions, and exception handling
- File handling and directory management
- The `pathlib` module
- Building interactive web applications using Streamlit
- Input validation and basic filesystem security
- Git and GitHub project documentation

## 🔮 Future Improvements

- File upload and download functionality
- Search and filter files
- Create and manage folders
- File previews and editing
- Support for additional file formats
- User authentication
- Online deployment

## 👨‍💻 Author

**Anirudh Pratap Singh**

GitHub: [https://github.com/Anirudh0024](https://github.com/Anirudh0024)
