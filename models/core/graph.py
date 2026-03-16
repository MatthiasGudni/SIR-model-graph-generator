import matplotlib.pyplot as plt


def setup_graph(title, N, days,
                xlabel="Dage",
                ylabel="Antal personer",
                figsize=(10, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlim(0, days)
    ax.set_ylim(0, N * 1.05)
    ax.grid(alpha=0.3)
    return fig, ax