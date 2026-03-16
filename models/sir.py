from .core import run_model

def sir(N, beta, gamma, days, I0, S0, R0, output_filename="sir_model.png"):
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
            {"label": "Inficerede (I)", "y0": I0},
            {"label": "Fjernede/Døde (R)", "y0": R0},
        ],
        params={"β": beta, "γ": gamma},
        days=days,
        output_filename=output_filename,
        infected_index=1,
        annotations=[{"text": f"R₀ = β/γ = {beta/gamma:.2f}", "x": 0.98, "y": 0.95}],
    )
