from .core import run_model

def sir(N, beta, gamma, days, I0, S0, R0, output_filename="sir_model.png", showRe=False):
    def ode(y, t, p):
        S, I, R = y
        dS = -p["β"] * S * I / N
        dI =  p["β"] * S * I / N - p["γ"] * I
        dR =  p["γ"] * I
        return [dS, dI, dR]

    run_model(
        name="SIR",
        ode_func=ode,
        compartments=[
            {"label": "Modtagelige (S)", "y0": S0},
            {"label": "Smittede (I)", "y0": I0},
            {"label": "Fjernede/Døde (R)", "y0": R0},
        ],
        params={"β": beta, "γ": gamma},
        days=days,
        output_filename=output_filename,
        infected_index=1,
        annotations=[{"text": f"R₀ = {beta/gamma:.2f}", "x": 0.98, "y": 0.95}, {"text": f"HIT = {(1 - gamma / beta) * 100:.2f}%", "x": 0.98, "y": 0.90}],
        showRe=showRe,
        re_func=lambda sol, t, p, N: (p["β"] / p["γ"]) * sol.T[0] / N,
    )
