import threading
import time
import tkinter as tk
from tkinter import font, ttk


class GDriveToolkitApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("GDrive ToolKit v1.0")
        self.geometry("1100x650")
        self.configure(bg="#1e1e1e")  # Dark Theme Background

        # Font များ သတ်မှတ်ခြင်း
        self.title_font = font.Font(family="Segoe UI", size=14, weight="bold")
        self.normal_font = font.Font(family="Segoe UI", size=10)
        self.bold_font = font.Font(family="Segoe UI", size=10, weight="bold")
        self.large_font = font.Font(family="Segoe UI", size=22, weight="bold")

        self.setup_ui()

    def setup_ui(self):
        # 1. Top Navigation Bar
        nav_bar = tk.Frame(self, bg="#2d2d2d", height=45)
        nav_bar.pack(fill="x", side="top")

        # Button Style Dictionary (px, py နေရာတွင် padx, pady ဟု ပြင်ထားပါသည်)
        btn_style = {
            "bg": "#2d2d2d",
            "fg": "white",
            "activebackground": "#3e3e42",
            "activeforeground": "white",
            "bd": 0,
            "padx": 15,
            "pady": 8,
            "font": self.normal_font,
        }

        # Drive Size Button (Active Tab ဖြစ်သဖြင့် အရောင် သီးသန့် ပြောင်းလိုပါက config သုံးပါသည်)
        btn_drive = tk.Button(nav_bar, text="Drive Size", **btn_style)
        btn_drive.config(bg="#3e3e42")
        btn_drive.pack(side="left", padx=(10, 2), pady=5)

        btn_sync = tk.Button(nav_bar, text="Sync Tools", **btn_style)
        btn_sync.pack(side="left", padx=2, pady=5)

        btn_setting = tk.Button(nav_bar, text="Settings", **btn_style)
        btn_setting.pack(side="left", padx=2, pady=5)

        # 2. Main Content Container
        main_container = tk.Frame(self, bg="#1e1e1e")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        # Left Column: Drive List Panel
        self.setup_left_panel(main_container)

        # Right Column: Dashboard & Log Console
        self.setup_right_panel(main_container)

    def setup_left_panel(self, parent):
        left_frame = tk.Frame(parent, bg="#252526", width=420)
        left_frame.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left_frame.pack_propagate(False)

        # Header Label
        lbl_header = tk.Label(
            left_frame,
            text="Shared Drives List",
            bg="#252526",
            fg="white",
            font=self.title_font,
        )
        lbl_header.pack(anchor="w", padx=15, pady=12)

        # Scrollable Canvas for Drive Cards
        canvas = tk.Canvas(left_frame, bg="#252526", highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            left_frame, orient="vertical", command=canvas.yview
        )
        self.scrollable_frame = tk.Frame(canvas, bg="#252526")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=(0, 10))
        scrollbar.pack(side="right", fill="y")

        # Sample Drive Data (၁၀ ခု)
        self.drives_data = [
            ("Drive 1: GDrive A", "25.40 GB"),
            ("Drive 2: Project Drive B", "1.00 TB"),
            ("Drive 3: Backup C", "150.25 GB"),
            ("Drive 4: Data D", "400.10 GB"),
            ("Drive 5: Archive E", "1.00 TB"),
            ("Drive 6: Docs F", "30.50 GB"),
            ("Drive 7: Media G", "2.50 TB"),
            ("Drive 8: Client H", "200.00 GB"),
            ("Drive 9: Shared I", "80.75 GB"),
            ("Drive 10: Reports J", "1.05 TB"),
        ]

        # Populate Drive Cards
        for name, size in self.drives_data:
            self.create_drive_card(self.scrollable_frame, name, size)

    def create_drive_card(self, parent, name, size):
        card = tk.Frame(parent, bg="#333333", height=45, width=370)
        card.pack(fill="x", expand=True, pady=4, padx=5)
        card.pack_propagate(False)

        # Cloud Icon Text
        lbl_icon = tk.Label(
            card, text="☁", bg="#333333", fg="#007acc", font=("Segoe UI", 14)
        )
        lbl_icon.pack(side="left", padx=(10, 5))

        lbl_name = tk.Label(
            card, text=name, bg="#333333", fg="white", font=self.bold_font
        )
        lbl_name.pack(side="left", padx=5)

        lbl_size = tk.Label(
            card, text=size, bg="#333333", fg="#cccccc", font=self.normal_font
        )
        lbl_size.pack(side="right", padx=15)

    def setup_right_panel(self, parent):
        right_frame = tk.Frame(parent, bg="#1e1e1e")
        right_frame.pack(side="right", fill="both", expand=True)

        # Top Section: Donut Chart & Button
        chart_card = tk.Frame(right_frame, bg="#252526")
        chart_card.pack(fill="both", expand=True, pady=(0, 10))

        lbl_total_title = tk.Label(
            chart_card,
            text="TOTAL SIZE ACROSS ALL DRIVES",
            bg="#252526",
            fg="#aaaaaa",
            font=self.bold_font,
        )
        lbl_total_title.pack(pady=(15, 5))

        # Donut Chart Canvas
        self.chart_canvas = tk.Canvas(
            chart_card, bg="#252526", width=260, height=220, highlightthickness=0
        )
        self.chart_canvas.pack(pady=5)
        self.draw_donut_chart()

        # Calculate Size Button
        self.btn_calc = tk.Button(
            chart_card,
            text="Calculate Size",
            bg="#28a745",
            fg="white",
            activebackground="#218838",
            activeforeground="white",
            font=self.bold_font,
            bd=0,
            padx=20,
            pady=8,
            command=self.start_calculation,
        )
        self.btn_calc.pack(pady=(5, 15))

        # Bottom Section: Calculation Log Terminal
        log_card = tk.Frame(right_frame, bg="#252526")
        log_card.pack(fill="both", expand=True)

        lbl_log_title = tk.Label(
            log_card,
            text="--- Log Console ---",
            bg="#252526",
            fg="#888888",
            font=self.normal_font,
        )
        lbl_log_title.pack(anchor="w", padx=15, pady=(10, 0))

        self.log_text = tk.Text(
            log_card,
            bg="#1e1e1e",
            fg="#00ff66",
            insertbackground="white",
            font=("Consolas", 9),
            bd=0,
        )
        self.log_text.pack(fill="both", expand=True, padx=15, pady=10)

        # Default Text
        self.log_text.insert(
            "1.0", "Ready to calculate total size...\nClick 'Calculate Size' to start.\n"
        )

    def draw_donut_chart(self):
        """Standard Tkinter Canvas ကိုသုံးပြီး Multi-color Donut Chart ဆွဲခြင်း"""
        c = self.chart_canvas
        c.delete("all")

        # Color segments ( degrees )
        segments = [
            (0, 90, "#2ecc71"),
            (90, 180, "#3498db"),
            (180, 240, "#f1c40f"),
            (240, 310, "#e67e22"),
            (310, 360, "#9b59b6"),
        ]

        # Draw Outer Ring Arcs
        for start, extent, color in segments:
            c.create_arc(
                25,
                10,
                235,
                210,
                start=start,
                extent=extent - start,
                fill=color,
                outline="",
            )

        # Draw Inner Circle to make it a Donut shape
        c.create_oval(55, 40, 205, 180, fill="#252526", outline="")

        # Center Text
        c.create_text(
            130,
            95,
            text="6.54 TB",
            fill="white",
            font=("Segoe UI", 20, "bold"),
        )
        c.create_text(
            130,
            125,
            text="10 of 10 Shared Drives\ncalculated.",
            fill="#aaaaaa",
            font=("Segoe UI", 8),
            justify="center",
        )

    def start_calculation(self):
        """Calculation Log တတ်လာစေရန် Simulation ပြုလုပ်ခြင်း"""
        self.btn_calc.config(state="disabled", bg="#555555")
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, "--- Calculation Started ---\n")

        threading.Thread(target=self.run_calc_process, daemon=True).start()

    def run_calc_process(self):
        total_size = 0.0
        for idx, (name, size_str) in enumerate(self.drives_data, start=1):
            time.sleep(0.4)
            current_time = time.strftime("%H:%M:%S")
            log_msg = f"[{idx}/10] {name} - {size_str} ({current_time})\n"

            self.log_text.insert(tk.END, log_msg)
            self.log_text.see(tk.END)

        self.log_text.insert(
            tk.END, "\n*** Total Size: 6.54 TB ***\nCalculation finished.\n"
        )
        self.btn_calc.config(state="normal", bg="#28a745")


if __name__ == "__main__":
    app = GDriveToolkitApp()
    app.mainloop()