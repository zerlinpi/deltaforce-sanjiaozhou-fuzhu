"""TacticalVision: standalone visualization laboratory.

Only simulated scene data is used. No process access, DMA, injected overlay,
automated aiming, device emulation, or game integration is performed.
"""
from __future__ import annotations

import math
import random
import tkinter as tk
from tkinter import ttk

BG = "#080e14"
PANEL = "#111d29"
EDGE = "#294455"
CYAN = "#29c7f9"
YELLOW = "#e9dd33"
WHITE = "#eaf5ff"
MUTED = "#91a8b7"
RED = "#ff5664"
GREEN = "#4ae6a2"


class TacticalVision(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TacticalVision Lab · Simulation Only")
        self.geometry("1330x820")
        self.minsize(1000, 650)
        self.configure(bg=BG)
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TNotebook", background=BG, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=PANEL, foreground=WHITE,
                             padding=(21, 11), font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", "#145572")])
        self.style.configure("TFrame", background=BG)
        self.style.configure("TCheckbutton", background=PANEL, foreground=WHITE)
        self.style.configure("TScale", background=PANEL)
        self.options = {}
        self.running = True
        self.ticks = 0
        self.rng = random.Random(13)
        self.entities = [(self.rng.uniform(-0.9, 0.9),
                          self.rng.uniform(-0.9, 0.9),
                          self.rng.choice(("Enemy", "Ally", "Loot")))
                         for _ in range(16)]
        top = tk.Frame(self, bg=BG, pady=14)
        top.pack(fill="x", padx=16)
        tk.Label(top, text="[TACTICAL] VISION LAB",
                 fg=YELLOW, bg=BG, font=("Segoe UI", 24, "bold")).pack(side="left")
        tk.Label(top, text="SIMULATED DATA  /  NO GAME CONNECTION",
                 fg=CYAN, bg=BG, font=("Consolas", 10)).pack(side="right")
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=16, pady=(0, 14))
        self.pages = {}
        for label in ("ESP", "AIM TRAINING", "CASE", "ITEM", "RADAR", "MISC"):
            frame = ttk.Frame(self.tabs)
            self.tabs.add(frame, text=label)
            self.pages[label] = frame
        self.build_esp()
        self.build_aim()
        self.build_case()
        self.build_item()
        self.build_radar()
        self.build_misc()
        self.status = tk.StringVar(value="Simulation running | 60 FPS target | No external data")
        tk.Label(self, textvariable=self.status, anchor="w", bg=PANEL,
                 fg=MUTED, padx=16, pady=8, font=("Consolas", 10)).pack(fill="x")
        self.after(30, self.update_scene)

    def panel(self, parent, title, side="left", width=260):
        frame = tk.Frame(parent, bg=PANEL, highlightbackground=EDGE,
                         highlightthickness=1, padx=15, pady=15, width=width)
        frame.pack(side=side, fill="y", padx=8, pady=9)
        frame.pack_propagate(False)
        tk.Label(frame, text=title, fg=CYAN, bg=PANEL,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 15))
        return frame

    def check(self, parent, label, default=True):
        var = tk.BooleanVar(value=default)
        tk.Checkbutton(parent, text=label, variable=var, selectcolor="#176588",
                       activebackground=PANEL, activeforeground=WHITE,
                       bg=PANEL, fg=WHITE, anchor="w",
                       font=("Segoe UI", 11)).pack(fill="x", pady=5)
        self.options[label] = var
        return var

    def scale(self, parent, label, start, end, value):
        tk.Label(parent, text=label, fg=WHITE, bg=PANEL,
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(12, 0))
        s = tk.Scale(parent, from_=start, to=end, orient="horizontal",
                     showvalue=True, resolution=1, bg=PANEL, fg=CYAN,
                     troughcolor="#334554", highlightthickness=0)
        s.set(value)
        s.pack(fill="x")
        return s

    def canvas_area(self, parent, heading):
        shell = tk.Frame(parent, bg=PANEL, highlightbackground=EDGE,
                         highlightthickness=1)
        shell.pack(side="left", fill="both", expand=True, padx=8, pady=9)
        tk.Label(shell, text=heading, bg=PANEL, fg=WHITE,
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=16, pady=12)
        canvas = tk.Canvas(shell, bg="#08141d", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        return canvas

    def build_esp(self):
        p = self.pages["ESP"]
        f = self.panel(p, "ESP Preview Settings", width=300)
        self.check(f, "Show simulated targets")
        self.check(f, "Show boxes")
        self.check(f, "Show names")
        self.check(f, "Show health bars")
        self.check(f, "Show distance")
        self.esp_range = self.scale(f, "Preview distance", 50, 800, 450)
        self.esp_canvas = self.canvas_area(p, "3D Scene Projection Preview · Synthetic Targets")

    def build_aim(self):
        p = self.pages["AIM TRAINING"]
        f = self.panel(p, "Offline Target Training", width=310)
        self.check(f, "Show crosshair guide")
        self.check(f, "Show practice markers")
        self.scale(f, "Practice target size", 4, 40, 18)
        self.aim_canvas = self.canvas_area(p, "Non-interactive Training Diagram")
        self.aim_canvas.bind("<Configure>", self.draw_aim)

    def draw_aim(self, _event=None):
        c = self.aim_canvas
        w, h = c.winfo_width(), c.winfo_height()
        c.delete("all")
        if w < 50 or h < 50:
            return
        cx, cy = w/2, h/2
        for r in (50, 110, 185):
            c.create_oval(cx-r, cy-r, cx+r, cy+r, outline=EDGE, width=2)
        c.create_line(cx-22, cy, cx+22, cy, fill=CYAN, width=2)
        c.create_line(cx, cy-22, cx, cy+22, fill=CYAN, width=2)
        c.create_text(cx, h-35, text="Visual training only — no mouse control",
                      fill=MUTED, font=("Consolas", 12))

    def build_case(self):
        p = self.pages["CASE"]
        f = self.panel(p, "Container Categories", width=300)
        for name in ("Weapon box", "Ammo box", "Medical crate",
                     "Toolbox", "Supply case", "Storage locker"):
            self.check(f, name)
        self.case_canvas = self.canvas_area(p, "Example Container Catalog")
        self.case_canvas.bind("<Configure>", lambda e: self.draw_catalog(self.case_canvas,
                 ["WEAPON", "AMMO", "MEDICAL", "TOOLS", "SUPPLIES", "STORAGE"]))

    def build_item(self):
        p = self.pages["ITEM"]
        f = self.panel(p, "Item Filter", width=300)
        for name in ("Equipment", "Weapons", "Medical", "Materials", "High rarity"):
            self.check(f, name)
        self.item_canvas = self.canvas_area(p, "Sample Item Catalog")
        self.item_canvas.bind("<Configure>", lambda e: self.draw_catalog(self.item_canvas,
                 ["ARMOR", "RIFLE", "MEDKIT", "CPU", "RADIO", "KEYCARD", "TOOL", "BATTERY"]))

    def draw_catalog(self, c, names):
        c.delete("all")
        w = max(400, c.winfo_width())
        cols = max(2, int(w // 175))
        for i, name in enumerate(names):
            x, y = 24+(i%cols)*165, 26+(i//cols)*155
            c.create_rectangle(x, y, x+144, y+130, fill="#183041", outline=EDGE, width=2)
            c.create_rectangle(x+45, y+20, x+99, y+76, fill="#2b5369", outline=CYAN)
            c.create_text(x+72, y+105, text=name, fill=WHITE,
                          font=("Consolas", 11, "bold"))

    def build_radar(self):
        p = self.pages["RADAR"]
        f = self.panel(p, "Radar Settings", width=300)
        self.check(f, "Show enemies")
        self.check(f, "Show allies")
        self.check(f, "Show loot")
        self.radar_range = self.scale(f, "Radar radius", 100, 1000, 500)
        self.check(f, "Rotate radar", default=True)
        self.radar_canvas = self.canvas_area(p, "2D Radar · Synthetic Position Stream")

    def build_misc(self):
        p = self.pages["MISC"]
        f = self.panel(p, "System", width=350)
        self.check(f, "Enable animation")
        self.check(f, "Show diagnostics")
        tk.Button(f, text="Pause / Resume simulation", bg="#14618b",
                  fg=WHITE, relief="flat", pady=10,
                  command=self.toggle_simulation).pack(fill="x", pady=20)
        box = self.canvas_area(p, "Data Source and Architecture")
        box.bind("<Configure>", lambda e: self.draw_info(box))

    def draw_info(self, c):
        c.delete("all")
        lines = ("DATA SOURCE: BUILT-IN SYNTHETIC ENTITIES",
                 "RENDERER: TKINTER CANVAS",
                 "GAME PROCESS MEMORY: NOT ACCESSED",
                 "DMA / DRIVER / KMBOX: NOT CONNECTED",
                 "NETWORK: NONE",
                 "PURPOSE: UI AND DATA VISUALIZATION TESTING")
        for i, line in enumerate(lines):
            c.create_text(35, 55+i*50, anchor="w", text=line, fill=CYAN if i == 0 else WHITE,
                          font=("Consolas", 12))

    def toggle_simulation(self):
        self.running = not self.running

    def update_scene(self):
        if self.running:
            self.ticks += 1
        self.draw_esp()
        self.draw_radar()
        self.status.set(f"Simulation {'running' if self.running else 'paused'}"
                        f" | frame {self.ticks} | entities {len(self.entities)}"
                        " | offline preview")
        self.after(33, self.update_scene)

    def draw_esp(self):
        c = self.esp_canvas
        w, h = c.winfo_width(), c.winfo_height()
        if w < 50 or h < 50:
            return
        c.delete("all")
        c.create_line(0, h*.7, w, h*.7, fill=EDGE, width=2)
        for i in range(12):
            x = i*w/11
            c.create_line(w/2, h*.45, x, h, fill="#173041")
        for i, (x, y, kind) in enumerate(self.entities[:10]):
            if not self.options["Show simulated targets"].get():
                break
            phase = self.ticks*.012+i
            px = w*(.5+x*.35)+math.sin(phase)*12
            py = h*(.49+y*.2)
            height = 55+(i%4)*18
            color = RED if kind == "Enemy" else GREEN if kind == "Ally" else YELLOW
            if self.options["Show boxes"].get():
                c.create_rectangle(px-20, py-height/2, px+20, py+height/2, outline=color, width=2)
            if self.options["Show names"].get():
                c.create_text(px, py-height/2-13, text=f"{kind.upper()} {i:02}",
                              fill=color, font=("Consolas", 10, "bold"))
            if self.options["Show health bars"].get() and kind != "Loot":
                c.create_rectangle(px-20, py+height/2+4, px+20, py+height/2+8,
                                   fill="#334455", outline="")
                c.create_rectangle(px-20, py+height/2+4, px+10, py+height/2+8,
                                   fill=GREEN, outline="")
            if self.options["Show distance"].get():
                c.create_text(px, py+height/2+21, text=f"{60+i*37} m",
                              fill=MUTED, font=("Consolas", 9))
        c.create_text(16, 18, anchor="w", fill=CYAN,
                      text="OFFLINE ESP VISUALIZER · GENERATED COORDINATES",
                      font=("Consolas", 11))

    def draw_radar(self):
        c = self.radar_canvas
        w, h = c.winfo_width(), c.winfo_height()
        if w < 50 or h < 50:
            return
        c.delete("all")
        cx, cy = w/2, h/2
        r = max(20, min(w, h)*.41)
        for scale in (.25, .5, .75, 1.0):
            q = r*scale
            c.create_oval(cx-q, cy-q, cx+q, cy+q, outline=EDGE, width=2)
        c.create_line(cx-r, cy, cx+r, cy, fill=EDGE)
        c.create_line(cx, cy-r, cx, cy+r, fill=EDGE)
        for a, word in ((0, "E"), (math.pi/2, "S"),
                        (math.pi, "W"), (math.pi*1.5, "N")):
            c.create_text(cx+(r+20)*math.cos(a), cy+(r+20)*math.sin(a),
                          text=word, fill=CYAN, font=("Consolas", 15, "bold"))
        angle = self.ticks*.008 if self.options["Rotate radar"].get() else 0
        for i, (x, y, kind) in enumerate(self.entities):
            if not self.options[{"Enemy":"Show enemies","Ally":"Show allies",
                                 "Loot":"Show loot"}[kind]].get():
                continue
            px = cx+r*(x*math.cos(angle)-y*math.sin(angle))
            py = cy+r*(x*math.sin(angle)+y*math.cos(angle))
            color = RED if kind == "Enemy" else GREEN if kind == "Ally" else YELLOW
            c.create_oval(px-5, py-5, px+5, py+5, fill=color, outline="")
        c.create_polygon(cx, cy-13, cx-8, cy+10, cx, cy+5, cx+8, cy+10, fill=WHITE)
        c.create_text(20, 20, anchor="w", fill=CYAN,
                      text=f"RANGE {self.radar_range.get()} m / SIMULATION",
                      font=("Consolas", 12))


if __name__ == "__main__":
    TacticalVision().mainloop()
