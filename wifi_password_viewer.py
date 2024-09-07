import subprocess
import tkinter as tk
from tkinter import messagebox

# Function to fetch Wi-Fi profiles and passwords
def get_wifi_passwords():
    try:
        # Get all Wi-Fi profiles
        wifi_profiles = subprocess.check_output("netsh wlan show profiles", shell=True).decode("utf-8")
        profile_names = [line.split(":")[1].strip() for line in wifi_profiles.split("\n") if "All User Profile" in line]

        # Collect profiles with their respective passwords
        wifi_details = []
        for profile in profile_names:
            profile_info = subprocess.check_output(f'netsh wlan show profile name="{profile}" key=clear', shell=True).decode("utf-8")
            password_line = [line.split(":")[1].strip() for line in profile_info.split("\n") if "Key Content" in line]
            password = password_line[0] if password_line else "No Password Found"
            wifi_details.append((profile, password))

        return wifi_details

    except Exception as e:
        messagebox.showerror("Error", f"Error fetching Wi-Fi passwords: {e}")
        return []

# Function to display Wi-Fi details in the GUI
def show_passwords():
    wifi_details = get_wifi_passwords()
    if wifi_details:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"{'Wi-Fi Network':<30}{'Password'}\n")
        result_text.insert(tk.END, "-" * 50 + "\n")
        for wifi_name, password in wifi_details:
            result_text.insert(tk.END, f"{wifi_name:<30}{password}\n")
    else:
        result_text.insert(tk.END, "No Wi-Fi passwords found.")

# Create the GUI window
root = tk.Tk()
root.title("Wi-Fi Password Viewer")
root.geometry("500x400")

# Title Label
title_label = tk.Label(root, text="Wi-Fi Password Viewer", font=("Helvetica", 16))
title_label.pack(pady=10)

# Button to show passwords
show_button = tk.Button(root, text="Show Saved Wi-Fi Passwords", command=show_passwords, font=("Helvetica", 12))
show_button.pack(pady=10)

# Textbox to display Wi-Fi passwords
result_text = tk.Text(root, width=60, height=15, font=("Courier", 10))
result_text.pack(pady=10)

# Start the GUI event loop
root.mainloop()
