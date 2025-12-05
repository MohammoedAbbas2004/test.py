import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

def ipr(q, Pr, qmax, Pwf0):
    return Pr - (q / qmax) * (Pr - Pwf0)

def vlp(q, tubing_diam, choke_size, fluid_density, viscosity, GOR, well_depth, Psurf):
    diam_ft = tubing_diam / 12
    area = np.pi * (diam_ft / 2)**2
    velocity = q * 5.615 / (86400 * area)
    friction_loss = 0.3164 * (velocity**2) * viscosity / (2 * diam_ft) * well_depth / 144
    choke_effect = choke_size * 10
    Pbh = Psurf + choke_effect + friction_loss + fluid_density * well_depth / 144
    return Pbh

def find_q(Pr, qmax, Pwf0, tubing_diam, choke_size, fluid_density, viscosity, GOR, well_depth, Psurf):
    def func(q):
        return ipr(q, Pr, qmax, Pwf0) - vlp(q, tubing_diam, choke_size, fluid_density, viscosity, GOR, well_depth, Psurf)
    q_guess = qmax / 2
    q_sol = fsolve(func, q_guess)[0]
    return max(0, q_sol)

def run_analysis():
    Pr = float(e_Pr.get())
    qmax = float(e_qmax.get())
    Pwf0 = float(e_Pwf0.get())
    tubing_diam = float(e_tubing.get())
    choke_size = float(e_choke.get())
    fluid_density = float(e_density.get())
    viscosity = float(e_visc.get())
    GOR = float(e_GOR.get())
    well_depth = float(e_depth.get())
    Psurf = float(e_psurf.get())

    q = find_q(Pr, qmax, Pwf0, tubing_diam, choke_size, fluid_density, viscosity, GOR, well_depth, Psurf)

    q_range = np.linspace(0, qmax, 100)
    ipr_curve = ipr(q_range, Pr, qmax, Pwf0)
    vlp_curve = [vlp(qi, tubing_diam, choke_size, fluid_density, viscosity, GOR, well_depth, Psurf) for qi in q_range]

    plt.figure(figsize=(7,5))
    plt.plot(q_range, ipr_curve, label="IPR")
    plt.plot(q_range, vlp_curve, label="VLP")
    plt.scatter(q, ipr(q, Pr, qmax, Pwf0), color="green", label=f"Intersection q={q:.1f}")
    plt.xlabel("Flow Rate (BBL/D)")
    plt.ylabel("Bottomhole Pressure (psi)")
    plt.legend()
    plt.grid()
    plt.show()

    lbl_result.config(text=f"Calculated q = {q:.1f} BBL/D")

root = tk.Tk()
root.title("Nodal Analysis – Simple Mode")
root.geometry("400x550")

params = [
    ("Reservoir Pressure Pr", "5000"),
    ("qmax (BBL/D)", "2000"),
    ("Pwf0", "500"),
    ("Tubing Diameter (in)", "2.5"),
    ("Choke Size (64th)", "64"),
    ("Fluid Density (lb/ft³)", "60"),
    ("Viscosity (cp)", "2"),
    ("GOR", "500"),
    ("Well Depth (ft)", "8000"),
    ("Surface Pressure", "100")
]

entries = []
for text, default in params:
    ttk.Label(root, text=text).pack()
    e = ttk.Entry(root)
    e.insert(0, default)
    e.pack()
    entries.append(e)

(e_Pr, e_qmax, e_Pwf0, e_tubing, e_choke, e_density, e_visc, e_GOR, e_depth, e_psurf) = entries

ttk.Button(root, text="Run Analysis", command=run_analysis).pack(pady=20)

lbl_result = ttk.Label(root, text="", font=("Arial", 12))
lbl_result.pack()

root.mainloop()
