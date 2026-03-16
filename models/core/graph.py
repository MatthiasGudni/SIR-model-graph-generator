import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def setup_graph(title, N, days,
                xlabel="Dage",
                ylabel="Antal personer",
                figsize=(13, 6)):
    fig = plt.figure(figsize=figsize)
    gs  = gridspec.GridSpec(1, 2, width_ratios=[5, 1], figure=fig,
                            wspace=0.02)

    ax       = fig.add_subplot(gs[0])
    ax_panel = fig.add_subplot(gs[1])

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlim(0, days)
    ax.set_ylim(0, N * 1.05)
    ax.grid(alpha=0.3)

    # Side panel: no axes, light background
    ax_panel.set_axis_off()
    ax_panel.set_facecolor("#f9f9f9")

    return fig, ax, ax_panel