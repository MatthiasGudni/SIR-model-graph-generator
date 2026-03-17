from .core.model import CompartmentalModel


class SimpleSI(CompartmentalModel):
    """Den mest enkelte SI-model (uden genopretning)"""

    def __init__(self, N, beta, I0, S0):
        self.N = N
        self.beta = beta
        self.I0 = I0
        self.S0 = S0

    def _build(self):
        N, beta = self.N, self.beta

        def ode(y, t, p):
            S, I = y
            dS = -p["β"] * S * I / N
            dI =  p["β"] * S * I / N
            return [dS, dI]

        return dict(
            name="SI",
            ode_func=ode,
            compartments=[
                {"label": "Modtagelige (S)", "y0": self.S0},
                {"label": "Smittede (I)",    "y0": self.I0},
            ],
            params={"β": beta},
            infected_index=1,
        )