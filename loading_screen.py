#!/usr/bin/env python3

import tkinter as tk
import requests
import re
import sys

# --- Configuration ---
I2PD_CONSOLE_URL = "http://127.0.0.1:7070/"
I2PD_PROXY_URL = "http://127.0.0.1:4444"
TEST_I2P_URL = "http://7tbay5p4kzeekxvyvbf6v7eauazemsnnl2aoyqhg5jzpr5eke7tq.b32.i2p/home.html"

# --- Behavior Tuning ---
TARGET_SUCCESS_RATE = 10.0      # Required tunnel rate to pass stage 1
NETWORK_CHECK_INTERVAL_MS = 500 # How often to check network status in the background
ANIMATION_INTERVAL_MS = 500      # How often to update the smooth progress bar

# --- UI Configuration ---
WINDOW_TITLE = "i2pd Initializing..."
PROGRESS_FONT = ("monospace", 40, "bold")
STATUS_FONT = ("monospace", 14)
BACKGROUND_COLOR = "black"
PROGRESS_BAR_COLOR = "red"
TEXT_COLOR = "white"

# --- Main Application ---
class LoadingScreen:
    def __init__(self, master):
        self.master = master
        self.master.title(WINDOW_TITLE)
        self.master.configure(bg=BACKGROUND_COLOR)
        self.master.attributes('-fullscreen', True)

        # State management
        self.progress = 0
        self.stage = 1  # 1: Tunnel check, 2: Proxy check, 3: Done

        # --- UI Elements ---
        self.center_frame = tk.Frame(master, bg=BACKGROUND_COLOR)
        self.center_frame.pack(expand=True)

        self.status_label = tk.Label(
            self.center_frame, text="Waiting for i2pd to start...",
            font=STATUS_FONT, fg=TEXT_COLOR, bg=BACKGROUND_COLOR
        )
        self.status_label.pack(pady=10)

        # Progress bar
        self.progress_frame = tk.Frame(
            self.center_frame, background=BACKGROUND_COLOR,
            width=800, height=100,
            highlightbackground=TEXT_COLOR, highlightthickness=2
        )
        self.progress_frame.pack(pady=20, padx=20)
        self.progress_frame.pack_propagate(False)

        self.progress_bar_canvas = tk.Canvas(
            self.progress_frame, bg=BACKGROUND_COLOR,
            width=800, height=100, highlightthickness=0
        )
        self.progress_bar_canvas.pack()

        self.progress_label = tk.Label(
            self.center_frame, text="0%",
            font=PROGRESS_FONT, fg=TEXT_COLOR, bg=BACKGROUND_COLOR
        )
        self.progress_label.pack(pady=10)

        # Start the update loops
        self.schedule_network_check()
        self.schedule_animation()

    def schedule_network_check(self):
        self.master.after(NETWORK_CHECK_INTERVAL_MS, self.check_network_status)

    def schedule_animation(self):
        self.master.after(ANIMATION_INTERVAL_MS, self.animate_progress)

    def check_network_status(self):
        """Checks network readiness in the background, acts as a 'gate' for stages."""
        if self.stage == 1:
            try:
                response = requests.get(I2PD_CONSOLE_URL, timeout=2)
                if response.status_code == 200:
                    match = re.search(r'<b>Tunnel creation success rate:</b> ([\d.]+)%', response.text)
                    if match and float(match.group(1)) >= TARGET_SUCCESS_RATE:
                        self.stage = 2  # Gate passed, move to stage 2
            except requests.exceptions.RequestException:
                pass  # Ignore errors, the animation loop will show a waiting state

        elif self.stage == 2:
            try:
                proxies = {'http': I2PD_PROXY_URL, 'https': I2PD_PROXY_URL}
                response = requests.get(TEST_I2P_URL, proxies=proxies, timeout=20)
                if response.status_code == 200:
                    self.stage = 3 # Gate passed, we are done
                    return # Stop rescheduling
            except requests.exceptions.RequestException:
                pass # Ignore errors, let it retry

        self.schedule_network_check() # Reschedule for the next check

    def animate_progress(self):
        """Animates the progress bar for a better user experience."""
        if self.stage == 1:
            self.status_label.config(text="Initializing I2P connection...")
            # Animate slowly up to 49% while waiting for the gate
            if self.progress < 49:
                self.progress += 0.5
        
        elif self.stage == 2:
            self.status_label.config(text="Verifying network access...")
            # Jump to 50% if we just passed stage 1, then animate to 99%
            if self.progress < 50:
                self.progress = 50
            elif self.progress < 99:
                self.progress += 0.5

        elif self.stage == 3:
            self.status_label.config(text="Success! Starting Firefox...")
            self.progress = 100
            self.update_ui()
            self.master.after(1000, self.quit_app)
            return # Stop the animation loop

        self.update_ui()
        self.schedule_animation()

    def update_ui(self):
        """Updates all visual elements based on the current progress."""
        display_progress = int(self.progress)
        self.progress_label.config(text=f"{display_progress}%")
        
        bar_width = self.progress_frame.winfo_width()
        fill_width = (self.progress / 100.0) * bar_width
        
        self.progress_bar_canvas.delete("all")
        self.progress_bar_canvas.create_rectangle(
            0, 0, fill_width, 100, fill=PROGRESS_BAR_COLOR, outline=""
        )

    def quit_app(self):
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoadingScreen(root)
    root.mainloop()
    sys.exit(0)