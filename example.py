import time
from models import SI, SIR, SIRDemography


def plot():
    t_all = time.time()

    SI(N=1000, beta=0.3, gamma=0.1, I0=1,
        S0=999).run(days=100, showRe=True,
        output="si_example.png")


    SIR(N=1000, beta=0.5, gamma=0.05, I0=1,
        S0=999, R0=0).run(days=200, showRe=True,
        output="sir_example.png")


    SIRDemography(N=1000, Alpha=10, beta=0.3, gamma=0.1,
        mu=0.01, I0=1, S0=999, R0=0).run(days=300, showRe=True,
        output="sir_demography_example.png")

    print(f"\nAll done in {time.time() - t_all:.2f}s")

if __name__ == "__main__":
    plot()