#!/usr/bin/env python3
"""
AIForeman - Local AI Services Manager
Version: 0.1.0 (Alpha)
Author: Grok + User
Date: 2026-05-10

Main GUI entry point for managing local AI stack (Ollama, Open WebUI, etc.)
"""

import customtkinter as ctk
from tkinter import ttk
import psutil
import subprocess
import json
import os
from datetime import datetime

# ================================================
# CONFIGURATION
# ================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AIForeman(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AIForeman - Local AI Manager")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # Load config
        self.config = self.load_config()

        self.build_ui()

    def load_config(self):
        """Load or create configuration"""
        config_path = "config.json"
        default_config = {
            "version": "0.1.0",
            "last_updated": datetime.now().isoformat(),
            "services": {}
        }

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except:
                return default_config
        else:
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config

    def build_ui(self):
        """Build the main interface"""
        # Title
        title = ctk.CTkLabel(self, text="AIForeman", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=20)

        subtitle = ctk.CTkLabel(self, text="Local AI Services Manager", font=ctk.CTkFont(size=16))
        subtitle.pack(pady=(0, 30))

        # ================================================
        # STATUS FRAME
        # ================================================
        status_frame = ctk.CTkFrame(self)
        status_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(status_frame, text="System Status", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=20, pady=10)

        # We'll add service status widgets here in next iterations

        # Placeholder for now
        placeholder = ctk.CTkLabel(status_frame, text="→ Services will appear here", text_color="gray")
        placeholder.pack(pady=30)

        # ================================================
        # CONTROL BUTTONS
        # ================================================
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkButton(btn_frame, text="Start Ollama", width=200, height=40, 
                     command=self.start_ollama).pack(side="left", padx=10)
        
        ctk.CTkButton(btn_frame, text="Stop Ollama", width=200, height=40, 
                     fg_color="red", command=self.stop_ollama).pack(side="left", padx=10)

        # TODO: Add more service buttons later

    def start_ollama(self):
        """Start Ollama service"""
        try:
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Ollama started")
        except Exception as e:
            print(f"Error starting Ollama: {e}")

    def stop_ollama(self):
        """Stop Ollama"""
        try:
            subprocess.run(["pkill", "-9", "-f", "ollama serve"], check=False)
            print("Ollama stopped")
        except Exception as e:
            print(f"Error stopping Ollama: {e}")


if __name__ == "__main__":
    app = AIForeman()
    app.mainloop()