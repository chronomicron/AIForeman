#!/usr/bin/env python3
"""
AIForeman - Local AI Services Manager
Version: 0.2.0
Goal: Clean, modular GUI to manage local AI stack

Layout:
- Top: Menu + Tabs
- Middle: Service-specific panel (changes per tab)
- Bottom: Console/Log output
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import psutil
import subprocess
import json
import os
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AIForeman(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AIForeman - Local AI Manager")
        self.geometry("1280x820")
        self.minsize(1100, 700)

        self.config = self.load_config()
        self.current_processes = {}

        self.build_ui()

    def load_config(self):
        config_path = "config.json"
        default = {
            "version": "0.2.0",
            "last_updated": datetime.now().isoformat(),
            "services": {}
        }
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        with open(config_path, 'w') as f:
            json.dump(default, f, indent=2)
        return default

    def build_ui(self):
        """Main UI Layout"""

        # ==================== TOP MENU ====================
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: print("AIForeman v0.2.0"))

        # ==================== TABS ====================
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: Ollama
        self.tab_ollama = self.tabview.add("Ollama")
        self.build_ollama_tab(self.tab_ollama)

        # Tab 2: Open WebUI
        self.tab_webui = self.tabview.add("Open WebUI")
        self.build_webui_tab(self.tab_webui)

        # Future tabs can be added easily here
        # self.tab_openclaw = self.tabview.add("OpenClaw")

        # ==================== BOTTOM CONSOLE ====================
        console_frame = ctk.CTkFrame(self, height=200)
        console_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(console_frame, text="Console / Log Output", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)

        self.console = ctk.CTkTextbox(console_frame, height=180)
        self.console.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.log("AIForeman v0.2.0 started successfully.")

    def log(self, message):
        """Print to console window"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.insert("end", f"[{timestamp}] {message}\n")
        self.console.see("end")

    # ====================== OLLAMA TAB ======================
    def build_ollama_tab(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Ollama Service", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Start Ollama", width=180, height=50,
                     command=self.start_ollama).pack(side="left", padx=15)

        ctk.CTkButton(btn_frame, text="Stop Ollama", width=180, height=50, fg_color="red",
                     command=self.stop_ollama).pack(side="left", padx=15)

    def start_ollama(self):
        try:
            subprocess.Popen(["ollama", "serve"])
            self.log("Ollama start command issued.")
        except Exception as e:
            self.log(f"Error starting Ollama: {e}")

    def stop_ollama(self):
        try:
            subprocess.run(["pkill", "-9", "-f", "ollama serve"], check=False)
            self.log("Ollama stop command sent.")
        except Exception as e:
            self.log(f"Error stopping Ollama: {e}")

    # ====================== WEBUI TAB ======================
    def build_webui_tab(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Open WebUI (Docker)", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Start WebUI", width=180, height=50,
                     command=self.start_webui).pack(side="left", padx=15)

        ctk.CTkButton(btn_frame, text="Stop WebUI", width=180, height=50, fg_color="red",
                     command=self.stop_webui).pack(side="left", padx=15)

    def start_webui(self):
        self.log("Starting Open WebUI (Docker)...")
        # We'll expand this with the full docker command later

    def stop_webui(self):
        self.log("Stopping Open WebUI...")
        subprocess.run(["docker", "stop", "open-webui"], check=False)


if __name__ == "__main__":
    app = AIForeman()
    app.mainloop()