import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import time
from .graph import setup_graph

COLORS = ["#2196F3", "#F44336", "#4CAF50", "#FF9800", "#9C27B0", "#00BCD4"]

def run_model(name, ode_func, compartments, params, days, output_filename,
            infected_index=None, annotations=None):
    """
    Parameters:
        name             : Model name shown in console and graph title
        ode_func         : Function with signature f(y, t, params) → list of derivatives
        compartments     : List of dicts: [{"label": "Modtagelige (S)", "y0": 999}, ...]
        params           : Dict of model parameters, fx. {"β": 0.3, "γ": 0.05}
        days             : Number of days to simulate
        output_filename  : Path to save the output PNG
        infected_index   : Index of the infected compartment in the compartments list.
                            If set, adds "top inficerede" and "50% inficerede" annotations
                            automatically. E.g. infected_index=1 for SIR (S=0, I=1, R=2)
        annotations      : Optional list of dicts for extra text box annotations:
                            [{"text": "R₀=6.0", "x": 0.98, "y": 0.95}, ...]
    """
    t_start = time.time()
    param_str = ", ".join(f"{k}={v}" for k, v in params.items())
    print(f"\n[{name}] Starting: {param_str}, days={days} → {output_filename}")

    y0     = [c["y0"] for c in compartments]
    N      = sum(y0)
    labels = [c["label"] for c in compartments]

    print(f"[{name}] Solving ODE...")
    t        = np.linspace(0, days, days * 10)
    solution = odeint(ode_func, y0, t, args=(params,))
    print(f"[{name}] ODE solved in {time.time() - t_start:.2f}s")

    print(f"[{name}] Plotting...")
    fig, ax = setup_graph(
        title=f"{name} Epidemi Model",
        N=N, days=days
    )

    for i, (label, series) in enumerate(zip(labels, solution.T)):
        ax.plot(t, series, label=label, color=COLORS[i % len(COLORS)], linewidth=2)
    ax.legend(fontsize=11)

    # Display parameters (top-left)
    for i, (k, v) in enumerate(params.items()):
        ax.text(0.02, 0.95 - i * 0.07, f"{k} = {v}",
                transform=ax.transAxes, ha="left", va="top",
                fontsize=11, bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.7))

    # Auto-annotations
    if infected_index is not None:
        I       = solution.T[infected_index]
        I_color = COLORS[infected_index % len(COLORS)]

        # Top inficerede
        peak_day = t[np.argmax(I)]
        peak_val = np.max(I)
        ax.axvline(peak_day, color=I_color, linestyle="--", alpha=0.4)
        ax.annotate(f"Top: {peak_val:.0f} inficerede\n(dag {peak_day:.0f})",
                    xy=(peak_day, peak_val),
                    xytext=(peak_day + days * 0.04, peak_val * 0.95),
                    arrowprops=dict(arrowstyle="->", color="gray"),
                    fontsize=9, color="gray")

        # 50% inficerede
        half_idx = np.argmax(I >= N * 0.5)
        if half_idx > 0:
            half_day = t[half_idx]
            ax.axvline(half_day, color=I_color, linestyle=":", alpha=0.4)
            ax.annotate(f"50% inficerede\n(dag {half_day:.0f})",
                        xy=(half_day, N * 0.5),
                        xytext=(half_day + days * 0.04, N * 0.55),
                        arrowprops=dict(arrowstyle="->", color="gray"),
                        fontsize=9, color="gray")

    if annotations:
        for a in annotations:
            ax.text(a["x"], a["y"], a["text"],
                    transform=ax.transAxes, ha="right", va="top",
                    fontsize=11, bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.7))

    plt.tight_layout()
    plt.savefig(output_filename, dpi=150)
    plt.close()
    print(f"[{name}] Saved as {output_filename} (total: {time.time() - t_start:.2f}s)")
