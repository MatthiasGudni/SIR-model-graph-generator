import time
from models import SimpleSI, SI, SIR, SIRDemography

# Figurer til min SRP
simple_si_example = SimpleSI(N=1000, beta=0.3,I0=1, S0=999)
klassisk_sir_example = SIR(N=1000, beta=0.3, gamma=0.1, I0=1, S0=999, R0=0)

def plot():
    t_all = time.time()

    simple_si_example.run(
        days=50, output="../simple_si_example.png")

    klassisk_sir_example.run(
        days=200, showRe=True, output="../klassisk_sir_example.png")

    print(f"\nAll done in {time.time() - t_all:.2f}s")

if __name__ == "__main__":
    plot()