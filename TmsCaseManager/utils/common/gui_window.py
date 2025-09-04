import tkinter as tk
from tkinter import messagebox
import os
import subprocess
from login_helper import loginHelper
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))  #fixed

from features.listenerclass import CustomListener

# ================== Helper: Save credentials & environment ==================
def update_credentials(username: str, password: str, env: str, feature_file: str):
    # Go to project root (d:/TMS-CaseManager API (2))
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    
    # Always save inside TmsCaseManager folder
    target_dir = os.path.join(project_root, "TmsCaseManager")

    creds_path = os.path.join(target_dir, "credentialsWrite.txt")
    env_path   = os.path.join(target_dir, "environmentURLWrite.txt")

    with open(creds_path, "w") as f:
        f.write(f"Username={username}\nPassword={password}\nFeatureFile={feature_file}\n")

    with open(env_path, "w") as f:
        f.write(env)


# ================== Run Scenario Handler ==================
def run_scenario():
    selected = scenario_var.get()
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    

  # need to fix this

    # Get feature file directly from textbox
    feature_file = feature_entry.get().strip()
    if not feature_file.endswith(".feature"):
        messagebox.showerror("Error", "Feature file must end with .feature")
        return

    feature_path = os.path.join(project_root,"features",feature_file)
    print("Looking for feature at:", repr(feature_path))


    if not os.path.exists(os.path.join(project_root, feature_path)):
        messagebox.showerror("Error", f"Feature file not found: {feature_file}")
        return

    # Build Behave command
    if selected == "all":
        command = ["behave", "--no-capture", "TmsCaseManager/features/" + feature_file]
        messagebox.showinfo("Executing", f"Running command:\n{' '.join(command)}")
    else:
        name = specific_entry.get().strip()
        if not name:
            messagebox.showwarning("Missing Input", "Please enter a scenario name.")
            return
        command = ["behave", "--no-capture", "TmsCaseManager/features/", "-i", feature_file, "-n", name]
        messagebox.showinfo("Executing", f"Running command:\n{' '.join(command)}")

    try:
        print(f"Executing: {' '.join(command)}")

        # Run Behave and capture output
        repo_root = os.path.abspath(os.path.join(project_root, ".."))
        result = subprocess.run(command, cwd=repo_root, capture_output=True, text=True)

        # Print behave output to console
        print(result.stdout)

        # If specific scenario not found, trigger listener
        if "-n" in command:
            scenario_name = command[-1]
            if "0 scenarios passed" in result.stdout and "0 failed" in result.stdout:
                listener = CustomListener()
                listener.scenario_not_found(scenario_name)

        # ================== NEW: Run Allure Report if checkbox is ticked ==================
        if allure_var.get():
            bat_path = os.path.join(project_root, "run.bat")
            if os.path.exists(bat_path):
                subprocess.Popen([bat_path], cwd=project_root, shell=True)
                messagebox.showinfo("Allure Report", "Allure report generation started.")
            else:
                messagebox.showerror("Error", f"Batch file not found: {bat_path}")

    except Exception as e:
        messagebox.showerror("Execution Error", f"Something went wrong:\n{str(e)}")

    if not stay_var.get():
        root.destroy()

# ================== Switch to Scenario Runner ==================
def switch_to_scenario_screen():
    login_frame.pack_forget()
    scenario_frame.pack(fill="both", expand=True)

# ================== Login Logic ==================
def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    env = env_var.get().lower()
    feature_file = feature_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return
    if not feature_file.endswith(".feature"):
        messagebox.showerror("Error", "Please enter a valid feature file (must end with .feature).")
        return

    update_credentials(username, password, env, feature_file)

    try:
        token = loginHelper.TMS_CaseManagerLoginforGui()
        print(token)
        if token and isinstance(token, str) and len(token) > 20:
            messagebox.showinfo("Login Success", "Access Token received successfully!")
            root.clipboard_clear()
            root.clipboard_append(token)
            switch_to_scenario_screen()
        else:
            messagebox.showerror("Login Failed", "No token returned. Please check credentials.")
    except Exception as e:
        messagebox.showerror("Login Error", f"Login failed due to:\n{str(e)}")

# ================== Radio Button Logic ==================
def on_radio_select():
    specific_entry.pack_forget()
    run_button.pack_forget()
    stay_checkbox.pack_forget()
    allure_checkbox.pack_forget()
    if scenario_var.get() == "all":
        run_button.config(text="Run All Scenarios")
        run_button.pack(pady=10)
        stay_checkbox.pack()
        allure_checkbox.pack(pady=5)
    elif scenario_var.get() == "specific":
        specific_entry.pack(pady=10)
        run_button.config(text="Run Specific Scenario")
        run_button.pack(pady=10)
        stay_checkbox.pack()
        allure_checkbox.pack(pady=5)

# ================== GUI Setup Starts Here ==================
root = tk.Tk()
root.title("EMOT - TMS Launcher")
root.geometry("450x500")
root.configure(bg="white")

# ----- Login Frame -----
login_frame = tk.Frame(root, bg="white")
login_frame.pack(fill="both", expand=True)

tk.Label(login_frame, text="EMOT", font=("Arial", 24, "bold"), bg="white").pack(pady=(30, 5))
tk.Label(login_frame, text="Login to access your account and explore", font=("Arial", 10),
         bg="white", fg="gray").pack()

username_entry = tk.Entry(login_frame, font=("Arial", 12), bg="#eef3ff")
username_entry.insert(0, "demo_testuser2")
username_entry.pack(pady=10, ipady=8, ipadx=5)

password_entry = tk.Entry(login_frame, font=("Arial", 12), show="*", bg="#eef3ff")
password_entry.pack(pady=10, ipady=8, ipadx=5)

env_var = tk.StringVar(login_frame)
env_var.set("QA")
tk.OptionMenu(login_frame, env_var, "QA", "DEV").pack(pady=10)

# --- Feature file entry instead of dropdown ---
tk.Label(login_frame, text="Enter Feature File (e.g., case_manager.feature)",
         font=("Arial", 10), bg="white", fg="gray").pack()
feature_entry = tk.Entry(login_frame, font=("Arial", 12), bg="#eef3ff")
feature_entry.insert(0, "case_manager.feature")
feature_entry.pack(pady=10, ipady=8, ipadx=5)

tk.Button(login_frame, text="Sign In", font=("Arial", 12, "bold"),
          bg="#007b5e", fg="white", width=20, height=2,
          command=login).pack(pady=20)

# ----- Scenario Frame -----
scenario_frame = tk.Frame(root, bg="white")

tk.Label(scenario_frame, text="Run Automation", font=("Arial", 18, "bold"),
         bg="white").pack(pady=(40, 10))

scenario_var = tk.StringVar()
scenario_var.set("all")

tk.Radiobutton(scenario_frame, text="Run All Scenarios", variable=scenario_var, value="all",
               font=("Arial", 12), bg="white", command=on_radio_select).pack(pady=5)

tk.Radiobutton(scenario_frame, text="Run Specific Scenario", variable=scenario_var, value="specific",
               font=("Arial", 12), bg="white", command=on_radio_select).pack(pady=5)

specific_entry = tk.Entry(scenario_frame, font=("Arial", 12), width=30)

run_button = tk.Button(scenario_frame, text="Run", font=("Arial", 12),
                       bg="#007b5e", fg="white", command=run_scenario)

stay_var = tk.BooleanVar()
stay_checkbox = tk.Checkbutton(scenario_frame,
    text="Come back to this screen once run is completed",
    variable=stay_var, bg="white", font=("Arial", 9))

# ----- NEW: Allure Report Checkbox -----
allure_var = tk.BooleanVar()
allure_checkbox = tk.Checkbutton(scenario_frame,
    text="Generate Allure Report after execution",
    variable=allure_var, bg="white", font=("Arial", 9))

# ================== Start the GUI ==================
root.mainloop()
