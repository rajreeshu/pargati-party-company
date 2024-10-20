import subprocess
import tkinter as tk
from tkinter import messagebox


def check_git_status():
    # Run 'git pull' command and capture the output
    result = subprocess.run(['git', 'pull'], capture_output=True, text=True)

    # Check if the repository is already up-to-date
    if 'Already up to date' in result.stdout:
        show_message("Already Updated")
    else:
        show_message("Updated")


def show_message(message):
    # Create a Tkinter window and hide it
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Show the message box
    messagebox.showinfo("Git Status", message)

    # Destroy the window after message box is closed
    root.destroy()


if __name__ == "__main__":
    check_git_status()
