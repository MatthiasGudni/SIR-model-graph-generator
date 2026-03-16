from .core import run_model

def sir_demography(N, Alpha, beta, gamma, mu, days, I0, S0, R0, output_filename="sir_demography_model.png", showRe=False):
    def ode(y, t, p):
        S, I, R = y
        dS = p["Α"] -p["β"] * S * I / N - p["μ"] * S
        dI =  p["β"] * S * I / N - p["γ"] * I - p["μ"] * I
        dR =  p["γ"] * I - p["μ"] * R
        return [dS, dI, dR]

    run_model(
        name="SIR",
        ode_func=ode,
        compartments=[
            {"label": "Modtagelige (S)", "y0": S0},
            {"label": "Inficerede (I)", "y0": I0},
            {"label": "Fjernede/Døde (R)", "y0": R0},
        ],
        params={"Α": Alpha, "β": beta, "γ": gamma, "μ": mu},
        days=days,
        output_filename=output_filename,
        infected_index=1,
        annotations=[{"text": f"R₀ = β/γ = {beta/gamma:.2f}", "x": 0.98, "y": 0.95}],
        showRe=showRe,
        re_func=lambda sol, t, p, N: (p["β"] / (p["γ"] + p["μ"])) * sol.T[0] / N,
    )
