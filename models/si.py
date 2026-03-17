from .core.model import CompartmentalModel


class SI(CompartmentalModel):
    """Den klassiske SI-model (Kermack-McKendrick's model)"""

    def __init__(self, N, beta, gamma, I0, S0):
        self.N = N
        self.beta = beta
        self.gamma = gamma
        self.I0 = I0
        self.S0 = S0
        self.R_0 = beta / gamma
        self.HIT = (1 - gamma / beta) * 100

    def _build(self):
        N, beta, gamma = self.N, self.beta, self.gamma

        def ode(y, t, p):
            S, I = y
            dS = -p["β"] * S * I / N
            dI =  p["β"] * S * I / N - p["γ"] * I
            return [dS, dI]
        
        def re_func(sol, t, p, N):
            S = sol.T[0]
            return (p["β"] / p["γ"]) * S / N

        return dict(
            name="SI",
            ode_func=ode,
            compartments=[
                {"label": "Modtagelige (S)", "y0": self.S0},
                {"label": "Smittede (I)",    "y0": self.I0},
            ],
            params={"β": beta, "γ": gamma},
            infected_index=1,
            annotations=[
                {"text": f"R₀ = {self.R_0:.2f}",              "x": 0.98, "y": 0.95},
                {"text": f"HIT = {self.HIT:.2f}%", "x": 0.98, "y": 0.90},
            ],
            re_func=re_func,
        )