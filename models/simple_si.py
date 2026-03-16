from .core import run_model

def simple_si(N, beta, days, I0, S0, output_filename="si_model.png"):
    def ode(y, t, p):
        S, I = y
        dS = -p["β"] * S * I / N
        dI =  p["β"] * S * I / N
        return [dS, dI]

    run_model(
        name="SI",
        ode_func=ode,
        compartments=[
            {"label": "Modtagelige (S)", "y0": S0},
            {"label": "Inficerede (I)", "y0": I0},
        ],
        params={"β": beta},
        days=days,
        output_filename=output_filename,
        infected_index=1,
    )
