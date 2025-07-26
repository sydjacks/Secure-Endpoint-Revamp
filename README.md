# Secure-Endpoint-Revamp

This tool processes diagnostic ZIP or 7z files to extract and analyze log events,
specifically focusing on "Event::HandleCreation" entries. It identifies and summarizes
common processes, file paths, file extensions, and directory paths from the logs.

Key Features:
- Accepts a single diagnostic file or a directory of logs as input.
- Automatically detects and extracts logs from compressed archives.
- Organizes results into a timestamped subdirectory within a central "results" folder.
- Generates a human-readable summary file (-summary.txt) showing:
    • Top 10 most common processes
    • Top 10 accessed files
    • Top 10 file extensions
    • Top 100 accessed directories
- GUI integration allows users to select input files and view results in a styled Tkinter window.
- Optionally allows exporting the summary to a separate text file from the GUI.
- Optionally allows the user to input start time for analysis.


Future Installments:
- Results scrollbar
- Diagnostic Analyzer version name update
- Runtime optimization (get_latest_summary_path); 
    Suggestion: Clear results directory at start time, user has option to save results locally. 

Written by Sydney Jackson and Samiya Fyffe



<img width="695" height="434" alt="Screenshot 2025-07-26 at 1 55 28 AM" src="https://github.com/user-attachments/assets/3360b3d6-2414-40d0-93ed-20b582c37e65" />
