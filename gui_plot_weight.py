#!/usr/bin/env python3
"""
Tkinter GUI for the preemie weight plotting application.

Features:
- Select a CSV file containing baby weight data.
- Input the expected due date (YYYY-MM-DD).
- Plot the baby's weight curve together with Fenton growth percentiles
  inside the GUI using a Matplotlib canvas.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import matplotlib
matplotlib.use("TkAgg") # Set backend before importing pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import core functions from the existing script
from plot_weight import load_data, load_fenton_data, plot_data  # plot_data now returns a Figure


class WeightPlotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Preemie Weight Plotter")
        self.geometry("900x600")
        self._create_widgets()
        self.canvas = None  # Will hold the FigureCanvasTkAgg instance

    def _create_widgets(self):
        # Control panel
        ctrl_frame = tk.Frame(self)
        ctrl_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # CSV file selection
        tk.Label(ctrl_frame, text="Weight CSV:").grid(row=0, column=0, sticky="e")
        self.file_path_var = tk.StringVar()
        tk.Entry(ctrl_frame, textvariable=self.file_path_var, width=50).grid(
            row=0, column=1, padx=5
        )
        tk.Button(ctrl_frame, text="Browse...", command=self._browse_file).grid(
            row=0, column=2, padx=5
        )

        # Due date entry
        tk.Label(ctrl_frame, text="Due Date (YYYY-MM-DD):").grid(
            row=1, column=0, sticky="e"
        )
        self.due_date_var = tk.StringVar()
        tk.Entry(ctrl_frame, textvariable=self.due_date_var, width=20).grid(
            row=1, column=1, sticky="w", padx=5
        )

        # Plot button
        tk.Button(ctrl_frame, text="Plot", command=self._plot).grid(
            row=2, column=0, columnspan=3, pady=10
        )

        # Plot display area
        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

    def _browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select weight CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if file_path:
            self.file_path_var.set(file_path)

    def _clear_canvas(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

    def _plot(self):
        file_path = self.file_path_var.get().strip()
        due_date_str = self.due_date_var.get().strip()

        # Basic validation
        if not file_path:
            messagebox.showerror("Error", "Please select a weight CSV file.")
            return
        if not due_date_str:
            messagebox.showerror("Error", "Please enter the due date.")
            return
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Due date must be in YYYY-MM-DD format.")
            return

        # Load baby data
        try:
            baby_dates, baby_weights = load_data(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load weight data:\n{e}")
            return

        if not baby_dates:
            messagebox.showwarning("No Data", "No valid weight entries found.")
            return

        # Load Fenton growth curves
        try:
            fenton_data = load_fenton_data(due_date)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Fenton data:\n{e}")
            return

        # Generate figure
        try:
            fig = plot_data(baby_dates, baby_weights, fenton_data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate plot:\n{e}")
            return

        # Embed figure in Tkinter
        self._clear_canvas()
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def destroy(self):
        plt.close('all')  # Close all matplotlib figures
        super().destroy()


if __name__ == "__main__":
    app = WeightPlotApp()
    app.mainloop()
