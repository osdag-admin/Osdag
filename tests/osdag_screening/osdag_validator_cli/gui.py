# osdag_validator_cli/gui.py
"""
Small Tkinter GUI wrapper for osdag-validator (optional/demo).

Run (inside virtualenv):
    python -m osdag_validator_cli.gui
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any
from .cli import run_command

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("osdag-validator GUI")
        self.geometry("640x320")
        self.columnconfigure(0, weight=1)

        frame = ttk.Frame(self, padding=12)
        frame.grid(sticky="nsew")
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Command").grid(row=0, column=0, sticky="w")
        self.cmd_var = tk.StringVar(value="fu")
        ttk.Entry(frame, textvariable=self.cmd_var).grid(row=0, column=1, sticky="ew")

        ttk.Label(frame, text="Args (comma separated)").grid(row=1, column=0, sticky="w")
        self.args_var = tk.StringVar(value="410")
        ttk.Entry(frame, textvariable=self.args_var).grid(row=1, column=1, sticky="ew")

        ttk.Label(frame, text="Format").grid(row=2, column=0, sticky="w")
        self.format_var = tk.StringVar(value="text")
        ttk.Combobox(frame, textvariable=self.format_var, values=["text","json","csv"]).grid(row=2, column=1, sticky="w")

        run_btn = ttk.Button(frame, text="Run", command=self.run)
        run_btn.grid(row=3, column=0, columnspan=2, pady=8)

        self.out = tk.Text(frame, height=10)
        self.out.grid(row=4, column=0, columnspan=2, sticky="nsew")
        frame.rowconfigure(4, weight=1)

    def run(self):
        cmd = self.cmd_var.get().strip()
        args = [a.strip() for a in self.args_var.get().split(",") if a.strip()]
        res = run_command(cmd, args)
        self.out.delete("1.0", tk.END)
        self.out.insert(tk.END, str(res))

def main():
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"GUI failed: {e}")

if __name__ == "__main__":
    main()
