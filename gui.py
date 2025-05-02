import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading

def browse_file(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def browse_directory(entry):
    directory = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, directory)

def toggle_db_fields():
    """Enable/disable database fields based on selection."""
    if db_var.get() == "Yes":
        exist_db_entry.config(state="normal")
        new_db_entry.config(state="disabled")
    else:
        exist_db_entry.config(state="disabled")
        new_db_entry.config(state="normal")

def run_nextflow():
    script = script_entry.get()

    params = {
        "--ref": ref_entry.get(),
        "--ref_strain": ref_strain_entry.get(),
        "--datadir": datadir_entry.get(),
        "--fna_read": fna_read_entry.get(),
        "--read": read_entry.get(),
        "--read1": read1_entry.get(),
        "--read2": read2_entry.get(),
        "--reads": reads_entry.get(),
        "--main_db": main_db_entry.get(),
        "--output_dir": output_dir_entry.get(),
        "--snpEff_db": snpeff_entry.get(),
        "--chr_name": chromosome_entry.get()
    }

    # Database selection
    if db_var.get() == "Yes":
        params["--exist_db"] = exist_db_entry.get()
    else:
        params["--new_db"] = new_db_entry.get()

    # Check required fields
    required_fields = {
        "Nextflow Script": script,
        "Reference File": ref_entry.get(),
        "Output Directory": output_dir_entry.get()
    }
    missing_fields = [name for name, value in required_fields.items() if not value.strip()]
    
    if missing_fields:
        messagebox.showerror("Missing Fields", f"Please fill in the following fields:\n- " + "\n- ".join(missing_fields))
        return  

    # Build command, skipping empty values
    command_parts = [f"nextflow run {script}"]
    command_parts += [f"{key} '{value}'" for key, value in params.items() if value]

    # Add manual command at the end
    manual_command = manual_entry.get().strip()
    if manual_command:
        command_parts.append(manual_command)

    command = " ".join(command_parts)

    def execute_command():
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in iter(process.stdout.readline, ''):
            log_text.insert(tk.END, line)
            log_text.see(tk.END)  # Auto-scroll to latest output
            app.update_idletasks()

        for line in iter(process.stderr.readline, ''):
            log_text.insert(tk.END, line, "error")
            log_text.see(tk.END)
            app.update_idletasks()

        process.stdout.close()
        process.stderr.close()
        process.wait()

        messagebox.showinfo("Execution Completed", "Nextflow pipeline execution finished.")

    threading.Thread(target=execute_command, daemon=True).start()

app = tk.Tk()
app.title("Nextflow Pipeline GUI")

# Script selection
tk.Label(app, text="Nextflow Script*:").grid(row=0, column=0)
script_entry = tk.Entry(app, width=60)
script_entry.grid(row=0, column=1)
tk.Button(app, text="Browse", command=lambda: browse_file(script_entry)).grid(row=0, column=2)

# Reference file
tk.Label(app, text="Reference File*:").grid(row=1, column=0)
ref_entry = tk.Entry(app, width=60)
ref_entry.grid(row=1, column=1)
tk.Button(app, text="Browse", command=lambda: browse_file(ref_entry)).grid(row=1, column=2)

# Reference Strain
tk.Label(app, text="Reference Strain*:").grid(row=2, column=0)
ref_strain_entry = tk.Entry(app, width=60)
ref_strain_entry.grid(row=2, column=1)

# SnpEff Database
tk.Label(app, text="SnpEff Database*:").grid(row=15, column=0)
snpeff_entry = tk.Entry(app, width=60)
snpeff_entry.grid(row=15, column=1)

# Chromosome Name
tk.Label(app, text="Chromosome Name*:").grid(row=14, column=0)
chromosome_entry = tk.Entry(app, width=60)
chromosome_entry.grid(row=14, column=1)

# Data directory
tk.Label(app, text="Data Directory*:").grid(row=3, column=0)
datadir_entry = tk.Entry(app, width=60)
datadir_entry.grid(row=3, column=1)
tk.Button(app, text="Browse", command=lambda: browse_directory(datadir_entry)).grid(row=3, column=2)

# FNA Read
tk.Label(app, text="FNA Read:").grid(row=4, column=0)
fna_read_entry = tk.Entry(app, width=60)
fna_read_entry.grid(row=4, column=1)
tk.Button(app, text="Browse", command=lambda: browse_file(fna_read_entry)).grid(row=4, column=2)

# Single FASTQ Read
tk.Label(app, text="Single FASTQ Read:").grid(row=5, column=0)
read_entry = tk.Entry(app, width=60)
read_entry.grid(row=5, column=1)
tk.Button(app, text="Browse", command=lambda: browse_file(read_entry)).grid(row=5, column=2)

# Forward Read1
tk.Label(app, text="Forward Read1:").grid(row=6, column=0)
read1_entry = tk.Entry(app, width=60)
read1_entry.grid(row=6, column=1)
tk.Button(app, text="Browse", command=lambda: browse_file(read1_entry)).grid(row=6, column=2)

# Reverse Read2
tk.Label(app, text="Reverse Read2:").grid(row=7, column=0)
read2_entry = tk.Entry(app, width=60)
read2_entry.grid(row=7, column=1)
tk.Button(app, text="Browse", command=lambda: browse_file(read2_entry)).grid(row=7, column=2)


# Paired Reads
tk.Label(app, text="Paired Reads:").grid(row=8, column=0)
reads_entry = tk.Entry(app, width=60)
reads_entry.grid(row=8, column=1)
tk.Button(app, text="Browse", command=lambda: browse_file(reads_entry)).grid(row=8, column=2)

# Main Database
tk.Label(app, text="Main Database*:").grid(row=9, column=0)
main_db_entry = tk.Entry(app, width=60)
main_db_entry.grid(row=9, column=1)
tk.Button(app, text="Browse", command=lambda: browse_file(main_db_entry)).grid(row=9, column=2)

# Output Directory
tk.Label(app, text="Output Directory*:").grid(row=10, column=0)
output_dir_entry = tk.Entry(app, width=60)
output_dir_entry.grid(row=10, column=1)
tk.Button(app, text="Browse", command=lambda: browse_directory(output_dir_entry)).grid(row=10, column=2)

# Select Database Type
tk.Label(app, text="Use Existing Database?*").grid(row=11, column=0)
db_var = tk.StringVar(value="No")
yes_button = tk.Radiobutton(app, text="Yes", variable=db_var, value="Yes", command=toggle_db_fields)
no_button = tk.Radiobutton(app, text="No", variable=db_var, value="No", command=toggle_db_fields)
yes_button.grid(row=11, column=1)
no_button.grid(row=11, column=2)

# Existing Database Path
tk.Label(app, text="Existing Database Path:*").grid(row=12, column=0)
exist_db_entry = tk.Entry(app, width=60, state="disabled")
exist_db_entry.grid(row=12, column=1)
tk.Button(app, text="Browse", command=lambda: browse_file(exist_db_entry)).grid(row=12, column=2)

# New Database Path
tk.Label(app, text="New Database Path:*").grid(row=13, column=0)
new_db_entry = tk.Entry(app, width=60)
new_db_entry.grid(row=13, column=1)
tk.Button(app, text="Browse", command=lambda: browse_directory(new_db_entry)).grid(row=13, column=2)

# Additional Command
tk.Label(app, text="Additional Command:").grid(row=16, column=0)
manual_entry = tk.Entry(app, width=60)
manual_entry.grid(row=16, column=1)

# Output Log
tk.Label(app, text="Execution Log:").grid(row=18, column=0)
log_text = tk.Text(app, height=16, width=80)
log_text.grid(row=18, column=1, columnspan=2)

# Run Button
tk.Button(app, text="Run Nextflow", command=run_nextflow).grid(row=17, column=1)

# Initialize fields
toggle_db_fields()

app.mainloop()









