from .core.model import CompartmentalModel


class SIRDemography(CompartmentalModel):
    """SIR-model med demografi"""

    def __init__(self, N, Alpha, beta, gamma, mu, I0, S0, R0=0):
        self.N = N
        self.Alpha = Alpha
        self.beta = beta
        self.gamma = gamma
        self.mu = mu
        self.I0 = I0
        self.S0 = S0
        self.R0 = R0
        self.R_0 = beta / (gamma + mu)
        self.HIT = (1 - (gamma + mu) / beta) * 100

    def _build(self):
        N, beta, gamma, mu = self.N, self.beta, self.gamma, self.mu

        def ode(y, t, p):
            S, I, R = y
            dS = p["Α"] - p["β"] * S * I / N - p["μ"] * S
            dI =  p["β"] * S * I / N - p["γ"] * I - p["μ"] * I
            dR =  p["γ"] * I - p["μ"] * R
            return [dS, dI, dR]
        
        def re_func(sol, t, p, N):
            S = sol.T[0]
            return (p["β"] / (p["γ"] + p["μ"])) * S / N

        return dict(
            name="SIR med demografi",
            ode_func=ode,
            compartments=[
                {"label": "Modtagelige (S)",   "y0": self.S0},
                {"label": "Smittede (I)",       "y0": self.I0},
                {"label": "Fjernede/Døde (R)", "y0": self.R0},
            ],
            params={"Α": self.Alpha, "β": beta, "γ": gamma, "μ": mu},
            infected_index=1,
            annotations=[
                {"text": f"R₀ = {self.R_0:.2f}",              "x": 0.98, "y": 0.95},
                {"text": f"HIT = {self.HIT:.2f}%", "x": 0.98, "y": 0.90},
            ],
            re_func=re_func
        )
