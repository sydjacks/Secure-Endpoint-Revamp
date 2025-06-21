from pathlib import Path
import os
import tkinter as tk
import tkinter.filedialog as fd
import subprocess
import sys
from tkinter import Tk, ttk, Canvas, Entry, Text, Button, PhotoImage, Label, Toplevel, StringVar, IntVar, Checkbutton, messagebox, Scrollbar, Frame
from tkinter import Toplevel, Label

def open_popup(current_window, parent_window):
    # Hide results window
    current_window.withdraw()

    # Re-show the original GUI window
    if parent_window:
        parent_window.deiconify()

    # Close the results window entirely
    current_window.destroy()


def get_section_from_summary(subheading, filepath):
    # Check if file exists
    if not os.path.isfile(filepath):
        print(f"Error: '{filepath}' not found.")
        return []

    # Read and extract section
    lines = []
    with open(filepath, "r") as f:
        in_section = False
        for line in f:
            if line.strip() == subheading:
                in_section = True
                continue  # Skip the subheading itself
            if in_section:
                if line.strip().endswith(":") and line.strip() != subheading:
                    break
                if line.strip() == "":
                    continue
                lines.append(line.rstrip())
    return lines

def get_latest_summary_path():
    results_dir = Path.cwd() / "results"

    if not results_dir.exists() or not results_dir.is_dir():
        raise FileNotFoundError("No 'results' directory found.")

    # Get only timestamped subdirectories
    timestamped_dirs = [d for d in results_dir.iterdir() if d.is_dir()]
    if not timestamped_dirs:
        raise FileNotFoundError("No timestamped subdirectories found in 'results'.")

    # Use max() for better performance
    latest_dir = max(timestamped_dirs, key=lambda d: d.name)

    summary_path = latest_dir / "-summary.txt"
    if not summary_path.exists():
        raise FileNotFoundError(f"No summary.txt found in {latest_dir}")

    return summary_path


def launch_results_window(file_path, options, parent_window=None):
    result_win = Toplevel(parent_window)
    result_win.title("Results")
    result_win.geometry("1090x863")
    result_win.configure(bg="#FFFFFF")
    result_win.resizable(False, False)


    canvas = Canvas(
        result_win,
        bg="#FFFFFF",
        height=863,
        width=1090,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Header
    canvas.create_rectangle(0.0, 0.0, 1090.0, 112.0, fill="#0489BA", outline="")
    canvas.create_text(
        13.0, 18.0,
        anchor="nw",
        text="secure",
        fill="#FFFFFF",
        font=("CiscoSansTT", -60)
    )

    import tkinter.font as tkFont
    font_secure = tkFont.Font(family="Jomolhari Regular", size=60)
    width_secure = font_secure.measure("secure")
    canvas.create_text(
        13.0 + width_secure,
        18.0,
        anchor="nw",
        text="endpoint",
        fill="#FFFFFF",
        font=("CiscoSans", -60)
    )

    # Main Container
    canvas.create_rectangle(60.0, 207.0, 1020.0, 785.0, fill="#FFFFFF", outline="")
    canvas.create_rectangle(250.0, 243.5, 780.0, 295.5, fill="#FFFFFF", outline="")

    canvas.create_text(
        285.0, 137.0,
        anchor="nw",
        text="Diagnostic Analyzer Results",
        fill="#000000",
        font=("CiscoSansTT", 45 * -1)
    )

    # Checks for activated selection to display
    active_sections = []
    if options.get("processes"):
        active_sections.append("Processes:")
    if options.get("files"):
        active_sections.append("Files:")
    if options.get("extensions"):
        active_sections.append("Extensions:")
    if options.get("paths"):
        active_sections.append("Paths:")


    summary_path = get_latest_summary_path()
    summary_text = "\n\n".join(
        f"{heading}\n" + "\n".join(get_section_from_summary(heading, summary_path))
        for heading in active_sections
    )

    canvas.create_text(
        125.0, 320.0,
        anchor="nw",
        text=summary_text or "No results to display for selected options.",
        fill="#000000",
        font=("CiscoSansTT", -20),
        width=840
    )

    export_button = tk.Button(
        result_win,
        text="Export Results",
        command=lambda: popup_export_file(result_win, summary_text),
        bd=0,
        highlightthickness=0,
        relief="flat",
        bg="#FFFFFF",
        activebackground="#FFFFFF"
    )
    export_button.place(x=441.0, y=220.0, width=201.0, height=37.0)

    back_button= tk.Button(
        result_win, 
        text="Back",
        bd=0,
        command=lambda: open_popup(result_win, parent_window),
        highlightthickness=0,
        relief="flat",
        bg="#FFFFFF",
        activebackground="#FFFFFF"
    )
    back_button.place(
        x=999.0,
        y=67.58892822265625,
        width=64.6875,
        height=29.210041046142578
    )

# Allows user to save the results shown in a local .txt file. 
def popup_export_file(parent, content_to_export):
    popup = tk.Toplevel(parent)
    popup.title("Export Results")
    popup.geometry("400x200")
    label = tk.Label(popup, text="Click below to save your results file.")
    label.pack(pady=20)

    def save_file():
        file_path = fd.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, "w") as f:
                f.write(content_to_export)
            tk.Label(popup, text="File saved!", fg="green").pack()

    save_btn = tk.Button(popup, text="Save File", command=save_file)
    save_btn.pack(pady=10)

    close_btn = tk.Button(popup, text="Close", command=popup.destroy)
    close_btn.pack(pady=10)
