import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import time
from .graph import setup_graph

COLORS = ["#2196F3", "#F44336", "#4CAF50", "#FF9800", "#9C27B0", "#00BCD4"]

# Maps Unicode Greek letters (used as param keys) to mathtext equivalents
_GREEK = {
    "α": r"$\alpha$",  "β": r"$\beta$",   "γ": r"$\gamma$",
    "δ": r"$\delta$",  "ε": r"$\varepsilon$", "σ": r"$\sigma$",
    "μ": r"$\mu$",     "ρ": r"$\rho$",    "λ": r"$\lambda$",
}

def _math(key):
    """Return a mathtext-formatted string for a param key (italic)."""
    return _GREEK.get(key, f"${key}$")

def run_model(name, ode_func, compartments, params, days, output_filename,
            infected_index=None, annotations=None,
            showRe=False, re_func=None):
    """
    Parameters:
        name             : Model name shown in console and graph title
        ode_func         : Function with signature f(y, t, params) → list of derivatives
        compartments     : List of dicts: [{"label": "Modtagelige (S)", "y0": 999}, ...]
        params           : Dict of model parameters, fx. {"β": 0.3, "γ": 0.05}
        days             : Number of days to simulate
        output_filename  : Path to save the output PNG
        infected_index   : Index of the infected compartment in the compartments list.
                            If set, adds "top smittede" and "50% smittede" annotations
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
    fig, ax, ax_panel = setup_graph(
        title=f"{name} Epidemi Model",
        N=N, days=days
    )

    for i, (label, series) in enumerate(zip(labels, solution.T)):
        ax.plot(t, series, label=label, color=COLORS[i % len(COLORS)], linewidth=2)

    # ── Side panel (Parametre + Initialbetingelser) ─────────────────────────
    panel_lines = ["Parametre", "─" * 14, rf"$N$  =  {int(N)}"]
    for k, v in params.items():
        panel_lines.append(f"{_math(k)}  =  {v}")
    if annotations:
        panel_lines.append("")
        for a in annotations:
            panel_lines.append(a["text"])

    init_lines = ["Initialbetingelser", "─" * 14]
    for c in compartments:
        sym = c["label"].split("(")[-1].rstrip(")")
        init_lines.append(f"${sym}(0)$  =  {int(c['y0'])}")

    combined_lines = panel_lines + [""] + init_lines

    ax_panel.text(
        0.12, 0.97,
        "\n".join(combined_lines),
        transform=ax_panel.transAxes,
        ha="left", va="top",
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.6", fc="white", ec="#cccccc", linewidth=0.8),
    )

    # Auto-annotations
    if infected_index is not None:
        I       = solution.T[infected_index]
        I_color = COLORS[infected_index % len(COLORS)]

        def _x_text(day):
            """Offset text left or right of the marker, clamped inside the graph."""
            x_off = days * 0.04 if day < days * 0.65 else -days * 0.24
            return max(days * 0.01, min(day + x_off, days * 0.91))

        # ── Build annotation specs (position only, no drawing yet) ────────────
        ann_specs = []

        peak_day = t[np.argmax(I)]
        peak_val = np.max(I)
        ax.axvline(peak_day, color=I_color, linestyle="--", alpha=0.4)
        ann_specs.append({
            "label":  f"Top: {peak_val:.0f} smittede\n(dag {peak_day:.0f})",
            "xy":     (peak_day, peak_val),
            "x_text": _x_text(peak_day),
            "y_text": min(peak_val * 0.95, N * 0.85),
        })

        half_idx = np.argmax(I >= N * 0.5)
        if half_idx > 0:
            half_day = t[half_idx]
            ax.axvline(half_day, color=I_color, linestyle=":", alpha=0.4)
            ann_specs.append({
                "label":  f"50% smittede\n(dag {half_day:.0f})",
                "xy":     (half_day, N * 0.5),
                "x_text": _x_text(half_day),
                "y_text": N * 0.55,
            })

        # ── Resolve vertical overlaps ─────────────────────────────────────────
        # Estimated bounding box of a 2-line annotation at fontsize 9
        X_BOX = days * 0.20
        Y_BOX = N * 0.16
        for _ in range(10):   # iterate until settled
            for i in range(len(ann_specs)):
                for j in range(i + 1, len(ann_specs)):
                    a, b = ann_specs[i], ann_specs[j]
                    if (abs(a["x_text"] - b["x_text"]) < X_BOX and
                            abs(a["y_text"] - b["y_text"]) < Y_BOX):
                        push = (Y_BOX - abs(a["y_text"] - b["y_text"])) / 2 + N * 0.01
                        if a["y_text"] >= b["y_text"]:
                            ann_specs[i]["y_text"] = min(a["y_text"] + push, N * 0.94)
                            ann_specs[j]["y_text"] = max(b["y_text"] - push, N * 0.04)
                        else:
                            ann_specs[i]["y_text"] = max(a["y_text"] - push, N * 0.04)
                            ann_specs[j]["y_text"] = min(b["y_text"] + push, N * 0.94)

        # ── Draw all annotations ──────────────────────────────────────────────
        for spec in ann_specs:
            ax.annotate(
                spec["label"],
                xy=spec["xy"],
                xytext=(spec["x_text"], spec["y_text"]),
                arrowprops=dict(arrowstyle="->", color="gray"),
                fontsize=9, color="#333333",
                bbox=dict(boxstyle="round,pad=0.35", fc="white",
                          ec="#cccccc", alpha=0.9, linewidth=0.8),
            )

    ax.legend(fontsize=11)

    # ── Effective reproduction number R_e ───────────────────────────────────
    if showRe and re_func is not None:
        Re       = re_func(solution, t, params, N)
        re_color = "#FF5722"

        # ── Mini R_e panel below combined textbox ────────────────────────────
        combined_box_bottom = 0.97 - len(combined_lines) * 0.065 - 0.10
        mini_h   = 0.22
        mini_bot = max(combined_box_bottom - 0.06 - mini_h, 0.01)

        ax_mini = ax_panel.inset_axes((0.25, mini_bot, 0.70, mini_h))
        ax_mini.plot(t, Re, color=re_color, linewidth=1.0)
        ax_mini.axhline(1, color=re_color, linestyle=":", alpha=0.5, linewidth=0.8)
        ax_mini.set_xlim(0, days)
        ax_mini.set_ylim(bottom=0)
        ax_mini.set_title(r"ERN over tid", fontsize=8, pad=3, color="#333333")
        ax_mini.set_xlabel("Dage", fontsize=7, color="#555555")
        ax_mini.set_ylabel(r"$R_e$", fontsize=7, color="#555555")
        ax_mini.tick_params(labelsize=6, colors="#555555")
        ax_mini.spines[["top", "right"]].set_visible(False)
        ax_mini.grid(alpha=0.2)

        # ── Annotate the day R_e crosses below 1 ─────────────────────────────
        cross_idx = np.argmax(Re < 1)
        if cross_idx > 0:
            cross_day = t[cross_idx]
            cross_val = Re[cross_idx]
            # Place text left or right depending on position in graph
            x_off = days * 0.08 if cross_day < days * 0.6 else -days * 0.08
            x_text = float(np.clip(cross_day + x_off, days * 0.05, days * 0.88))
            y_lim  = ax_mini.get_ylim()[1]
            y_text = float(np.clip(cross_val + y_lim * 0.25, y_lim * 0.1, y_lim * 0.85))
            ax_mini.annotate(
                f"$R_e$ < 1\n(dag {cross_day:.0f})",
                xy=(cross_day, cross_val),
                xytext=(x_text, y_text),
                arrowprops=dict(arrowstyle="->", color="gray", lw=0.7),
                fontsize=6, color="#333333",
                bbox=dict(boxstyle="round,pad=0.3", fc="white",
                          ec="#cccccc", alpha=0.9, linewidth=0.6),
            )

    plt.tight_layout(pad=0)
    plt.savefig(output_filename, dpi=150, bbox_inches="tight", pad_inches=0)
    plt.close()
    print(f"[{name}] Saved as {output_filename} (total: {time.time() - t_start:.2f}s)")
