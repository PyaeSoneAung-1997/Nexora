# # import time
# # import tkinter as tk
# # from tkinter import ttk


# # class ProgressStylesApp(tk.Tk):

# #     def __init__(self):
# #         super().__init__()
# #         self.title("5 Types of Progress Bars")
# #         self.geometry("500x550")
# #         self.configure(bg="#1e1e1e")

# #         self.val = 0
# #         self.setup_ui()

# #     def setup_ui(self):
# #         # --- STYLE 1: Circular / Ring Progress (စက်ဝိုင်းပုံ) ---
# #         tk.Label(
# #             self,
# #             text="1. Circular Ring Progress",
# #             bg="#1e1e1e",
# #             fg="#aaaaaa",
# #             font=("Segoe UI", 10, "bold"),
# #         ).pack(anchor="w", padx=20, pady=(15, 5))

# #         self.cv_ring = tk.Canvas(
# #             self, bg="#1e1e1e", width=80, height=80, highlightthickness=0
# #         )
# #         self.cv_ring.pack()

# #         # --- STYLE 2: Segmented Blocks (အကွက်လိုက် Retro ပုံစံ) ---
# #         tk.Label(
# #             self,
# #             text="2. Segmented Block Progress",
# #             bg="#1e1e1e",
# #             fg="#aaaaaa",
# #             font=("Segoe UI", 10, "bold"),
# #         ).pack(anchor="w", padx=20, pady=(15, 5))

# #         self.block_frame = tk.Frame(self, bg="#1e1e1e")
# #         self.block_frame.pack(pady=5)
# #         self.blocks = []
# #         for i in range(10):  # 10 Blocks
# #             b = tk.Label(
# #                 self.block_frame, bg="#333333", width=3, height=1, bd=1, relief="solid"
# #             )
# #             b.pack(side="left", padx=2)
# #             self.blocks.append(b)

# #         # --- STYLE 3: Embedded Text Bar (အလယ်တွင် စာသားပါသည့် ပုံစံ) ---
# #         tk.Label(
# #             self,
# #             text="3. Text Inside Progress Bar",
# #             bg="#1e1e1e",
# #             fg="#aaaaaa",
# #             font=("Segoe UI", 10, "bold"),
# #         ).pack(anchor="w", padx=20, pady=(15, 5))

# #         self.cv_text_bar = tk.Canvas(
# #             self, bg="#1e1e1e", width=400, height=25, highlightthickness=0
# #         )
# #         self.cv_text_bar.pack(pady=5)

# #         # --- STYLE 4: Ultra-Thin Minimal Line (YouTube/Browser Line ပုံစံ) ---
# #         tk.Label(
# #             self,
# #             text="4. Ultra-Thin Minimal Line",
# #             bg="#1e1e1e",
# #             fg="#aaaaaa",
# #             font=("Segoe UI", 10, "bold"),
# #         ).pack(anchor="w", padx=20, pady=(15, 5))

# #         self.cv_thin = tk.Canvas(
# #             self, bg="#2a2a2a", width=400, height=4, highlightthickness=0
# #         )
# #         self.cv_thin.pack(pady=5)

# #         # --- STYLE 5: Classic Gradient Progress (Standard Pill) ---
# #         tk.Label(
# #             self,
# #             text="5. Gradient Solid Bar",
# #             bg="#1e1e1e",
# #             fg="#aaaaaa",
# #             font=("Segoe UI", 10, "bold"),
# #         ).pack(anchor="w", padx=20, pady=(15, 5))

# #         self.cv_solid = tk.Canvas(
# #             self, bg="#2a2a2a", width=400, height=14, highlightthickness=0
# #         )
# #         self.cv_solid.pack(pady=5)

# #         # Controls
# #         self.btn_run = tk.Button(
# #             self,
# #             text="Simulate Progress",
# #             bg="#007acc",
# #             fg="white",
# #             bd=0,
# #             padx=15,
# #             pady=6,
# #             command=self.animate,
# #         )
# #         self.btn_run.pack(pady=25)

# #         self.update_bars(0)

# #     def update_bars(self, percent):
# #         # 1. Ring Update
# #         self.cv_ring.delete("all")
# #         self.cv_ring.create_arc(
# #             10,
# #             10,
# #             70,
# #             70,
# #             start=90,
# #             extent=-(percent * 3.6),
# #             fill="#007acc",
# #             outline="",
# #         )
# #         self.cv_ring.create_oval(20, 20, 60, 60, fill="#1e1e1e", outline="")
# #         self.cv_ring.create_text(
# #             40,
# #             40,
# #             text=f"{int(percent)}%",
# #             fill="white",
# #             font=("Segoe UI", 9, "bold"),
# #         )

# #         # 2. Block Update
# #         active_blocks = int(percent / 10)
# #         for idx, block in enumerate(self.blocks):
# #             if idx < active_blocks:
# #                 block.config(bg="#2ecc71")
# #             else:
# #                 block.config(bg="#333333")

# #         # 3. Text Inside Bar Update
# #         self.cv_text_bar.delete("all")
# #         fill_width = (percent / 100) * 400
# #         self.cv_text_bar.create_rectangle(
# #             0, 0, 400, 25, fill="#333333", outline=""
# #         )
# #         self.cv_text_bar.create_rectangle(
# #             0, 0, fill_width, 25, fill="#e67e22", outline=""
# #         )
# #         self.cv_text_bar.create_text(
# #             200,
# #             12,
# #             text=f"Downloading... {int(percent)}%",
# #             fill="white",
# #             font=("Segoe UI", 9, "bold"),
# #         )

# #         # 4. Thin Line Update
# #         self.cv_thin.delete("all")
# #         self.cv_thin.create_rectangle(
# #             0, 0, fill_width, 4, fill="#ff0055", outline=""
# #         )

# #         # 5. Solid Bar Update
# #         self.cv_solid.delete("all")
# #         self.cv_solid.create_rectangle(
# #             0, 0, fill_width, 14, fill="#9b59b6", outline=""
# #         )

# #     def animate(self):
# #         for i in range(101):
# #             self.update_bars(i)
# #             self.update()
# #             time.sleep(0.03)


# # if __name__ == "__main__":
# #     app = ProgressStylesApp()
# #     app.mainloop()

# import time
# import tkinter as tk
# from tkinter import ttk


# class ProgressStylesApp(tk.Tk):

#     def __init__(self):
#         super().__init__()
#         self.title("5 Types of Progress Bars")
#         self.geometry("500x550")
#         self.configure(bg="#1e1e1e")

#         self.val = 0
#         self.setup_ui()

#     def setup_ui(self):
#         # --- STYLE 1: Circular / Ring Progress (စက်ဝိုင်းပုံ) ---
#         tk.Label(
#             self,
#             text="1. Circular Ring Progress",
#             bg="#1e1e1e",
#             fg="#aaaaaa",
#             font=("Segoe UI", 10, "bold"),
#         ).pack(anchor="w", padx=20, pady=(15, 5))

#         self.cv_ring = tk.Canvas(
#             self, bg="#1e1e1e", width=80, height=80, highlightthickness=0
#         )
#         self.cv_ring.pack()

#         # --- STYLE 2: Segmented Blocks (အကွက်လိုက် Retro ပုံစံ) ---
#         tk.Label(
#             self,
#             text="2. Segmented Block Progress",
#             bg="#1e1e1e",
#             fg="#aaaaaa",
#             font=("Segoe UI", 10, "bold"),
#         ).pack(anchor="w", padx=20, pady=(15, 5))

#         self.block_frame = tk.Frame(self, bg="#1e1e1e")
#         self.block_frame.pack(pady=5)
#         self.blocks = []
#         for i in range(10):  # 10 Blocks
#             b = tk.Label(
#                 self.block_frame, bg="#333333", width=3, height=1, bd=1, relief="solid"
#             )
#             b.pack(side="left", padx=2)
#             self.blocks.append(b)

#         # --- STYLE 3: Embedded Text Bar (အလယ်တွင် စာသားပါသည့် ပုံစံ) ---
#         tk.Label(
#             self,
#             text="3. Text Inside Progress Bar",
#             bg="#1e1e1e",
#             fg="#aaaaaa",
#             font=("Segoe UI", 10, "bold"),
#         ).pack(anchor="w", padx=20, pady=(15, 5))

#         self.cv_text_bar = tk.Canvas(
#             self, bg="#1e1e1e", width=400, height=25, highlightthickness=0
#         )
#         self.cv_text_bar.pack(pady=5)

#         # --- STYLE 4: Ultra-Thin Minimal Line (YouTube/Browser Line ပုံစံ) ---
#         tk.Label(
#             self,
#             text="4. Ultra-Thin Minimal Line",
#             bg="#1e1e1e",
#             fg="#aaaaaa",
#             font=("Segoe UI", 10, "bold"),
#         ).pack(anchor="w", padx=20, pady=(15, 5))

#         self.cv_thin = tk.Canvas(
#             self, bg="#2a2a2a", width=400, height=4, highlightthickness=0
#         )
#         self.cv_thin.pack(pady=5)

#         # --- STYLE 5: Classic Gradient Progress (Standard Pill) ---
#         tk.Label(
#             self,
#             text="5. Gradient Solid Bar",
#             bg="#1e1e1e",
#             fg="#aaaaaa",
#             font=("Segoe UI", 10, "bold"),
#         ).pack(anchor="w", padx=20, pady=(15, 5))

#         self.cv_solid = tk.Canvas(
#             self, bg="#2a2a2a", width=400, height=14, highlightthickness=0
#         )
#         self.cv_solid.pack(pady=5)

#         # Controls
#         self.btn_run = tk.Button(
#             self,
#             text="Simulate Progress",
#             bg="#007acc",
#             fg="white",
#             bd=0,
#             padx=15,
#             pady=6,
#             command=self.animate,
#         )
#         self.btn_run.pack(pady=25)

#         self.update_bars(0)

#     def update_bars(self, percent):
#         # 1. Ring Update
#         self.cv_ring.delete("all")
#         self.cv_ring.create_arc(
#             10,
#             10,
#             70,
#             70,
#             start=90,
#             extent=-(percent * 3.6),
#             fill="#007acc",
#             outline="",
#         )
#         self.cv_ring.create_oval(20, 20, 60, 60, fill="#1e1e1e", outline="")
#         self.cv_ring.create_text(
#             40,
#             40,
#             text=f"{int(percent)}%",
#             fill="white",
#             font=("Segoe UI", 9, "bold"),
#         )

#         # 2. Block Update
#         active_blocks = int(percent / 10)
#         for idx, block in enumerate(self.blocks):
#             if idx < active_blocks:
#                 block.config(bg="#2ecc71")
#             else:
#                 block.config(bg="#333333")

#         # 3. Text Inside Bar Update
#         self.cv_text_bar.delete("all")
#         fill_width = (percent / 100) * 400
#         self.cv_text_bar.create_rectangle(
#             0, 0, 400, 25, fill="#333333", outline=""
#         )
#         self.cv_text_bar.create_rectangle(
#             0, 0, fill_width, 25, fill="#e67e22", outline=""
#         )
#         self.cv_text_bar.create_text(
#             200,
#             12,
#             text=f"Downloading... {int(percent)}%",
#             fill="white",
#             font=("Segoe UI", 9, "bold"),
#         )

#         # 4. Thin Line Update
#         self.cv_thin.delete("all")
#         self.cv_thin.create_rectangle(
#             0, 0, fill_width, 4, fill="#ff0055", outline=""
#         )

#         # 5. Solid Bar Update
#         self.cv_solid.delete("all")
#         self.cv_solid.create_rectangle(
#             0, 0, fill_width, 14, fill="#9b59b6", outline=""
#         )

#     def animate(self):
#         for i in range(101):
#             self.update_bars(i)
#             self.update()
#             time.sleep(0.03)


# if __name__ == "__main__":
#     app = ProgressStylesApp()
#     app.mainloop()

import random
import tkinter as tk


class DownloadWidget(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Download Progress Widget")
        self.geometry("520x220")
        self.configure(bg="#141414")
        self.resizable(False, False)

        # Download Data
        self.percent = 82.0
        self.downloaded = 8.4
        self.total = 10.2

        # Speed graph data history (30 points)
        self.speed_history = [
            random.uniform(5, 12) for _ in range(20)
        ] + [random.uniform(18, 24) for _ in range(10)]

        self.setup_ui()
        self.animate()

    def setup_ui(self):
        # Card Main Frame
        self.card = tk.Frame(
            self, bg="#222222", bd=1, relief="solid", highlightthickness=0
        )
        self.card.pack(padx=15, pady=15, fill="both", expand=True)

        # 1. Top Progress Bar Canvas
        self.cv_progress = tk.Canvas(
            self.card, bg="#222222", height=26, highlightthickness=0
        )
        self.cv_progress.pack(fill="x", padx=15, pady=(15, 12))

        # 2. Details Container
        self.info_frame = tk.Frame(self.card, bg="#222222")
        self.info_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Left Info Column
        self.left_frame = tk.Frame(self.info_frame, bg="#222222")
        self.left_frame.pack(side="left", fill="both", expand=True)

        font_style = ("Segoe UI", 10)
        lbl_fg = "#dddddd"

        self.lbl_status = tk.Label(
            self.left_frame,
            text="Status:    Downloading...",
            bg="#222222",
            fg=lbl_fg,
            font=font_style,
            anchor="w",
        )
        self.lbl_status.pack(fill="x", pady=2)

        self.lbl_eta = tk.Label(
            self.left_frame,
            text="ETA:        00:15:30",
            bg="#222222",
            fg=lbl_fg,
            font=font_style,
            anchor="w",
        )
        self.lbl_eta.pack(fill="x", pady=2)

        self.lbl_progress = tk.Label(
            self.left_frame,
            text="Progress: 8.4 GB of 10.2 GB (82%)",
            bg="#222222",
            fg=lbl_fg,
            font=font_style,
            anchor="w",
        )
        self.lbl_progress.pack(fill="x", pady=2)

        # Right Info Column
        self.right_frame = tk.Frame(self.info_frame, bg="#222222")
        self.right_frame.pack(side="right", anchor="ne")

        self.lbl_speed = tk.Label(
            self.right_frame,
            text="Speed: 21.3 MiB/s",
            bg="#222222",
            fg="#42b866",
            font=("Segoe UI", 13, "bold"),
            anchor="e",
        )
        self.lbl_speed.pack(fill="x")

        self.lbl_sub = tk.Label(
            self.right_frame,
            text="Last 1 minute",
            bg="#222222",
            fg="#888888",
            font=("Segoe UI", 8),
            anchor="e",
        )
        self.lbl_sub.pack(fill="x", pady=(0, 4))

        # Line Graph Canvas
        self.cv_graph = tk.Canvas(
            self.right_frame,
            bg="#222222",
            width=160,
            height=45,
            highlightthickness=0,
        )
        self.cv_graph.pack(anchor="e")

    def draw_progress(self):
        self.cv_progress.delete("all")
        w = self.cv_progress.winfo_width()
        h = 26
        if w <= 1:
            w = 460

        # Background track
        self.draw_round_rect(
            self.cv_progress, 0, 0, w, h, radius=8, fill="#383838"
        )

        # Filled progress track
        fill_w = max(12, (self.percent / 100) * w)
        self.draw_round_rect(
            self.cv_progress, 0, 0, fill_w, h, radius=8, fill="#42b866"
        )

        # Text inside progress bar
        self.cv_progress.create_text(
            w / 2,
            h / 2,
            text=f"{int(self.percent)}%",
            fill="white",
            font=("Segoe UI", 10, "bold"),
        )

    def draw_graph(self):
        self.cv_graph.delete("all")
        gw = 160
        gh = 45

        num_points = len(self.speed_history)
        step_x = gw / (num_points - 1)
        max_val = 30.0  # Graph Y-axis maximum scale

        points = []
        for i, val in enumerate(self.speed_history):
            x = i * step_x
            y = gh - (val / max_val * (gh - 8)) - 2
            points.append((x, y))

        # Fill background under graph
        poly_points = [(0, gh)] + points + [(gw, gh)]
        flat_poly = [c for p in poly_points for c in p]
        self.cv_graph.create_polygon(flat_poly, fill="#1c3d27", outline="")

        # Line chart
        flat_line = [c for p in points for c in p]
        if len(flat_line) >= 4:
            self.cv_graph.create_line(
                flat_line, fill="#42b866", width=2, smooth=True
            )

    def draw_round_rect(self, canvas, x1, y1, x2, y2, radius=8, **kwargs):
        points = [
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    def animate(self):
        # Speed နှင့် Graph တန်ဖိုးများကို dynamic ရွေ့လျားပေးခြင်း
        new_speed = round(random.uniform(19.0, 24.5), 1)
        self.lbl_speed.config(text=f"Speed: {new_speed} MiB/s")

        self.speed_history.pop(0)
        self.speed_history.append(new_speed)

        # Progress တိုးမြှင့်ခြင်း
        if self.percent < 100:
            self.percent += 0.05
            self.downloaded = round((self.percent / 100) * 10.2, 1)
            self.lbl_progress.config(
                text=f"Progress: {self.downloaded} GB of 10.2 GB ({int(self.percent)}%)"
            )

        self.draw_progress()
        self.draw_graph()

        self.after(150, self.animate)


if __name__ == "__main__":
    app = DownloadWidget()
    app.mainloop()