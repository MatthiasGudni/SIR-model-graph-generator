import time
from models import si, sir

def plot():
    t_all = time.time()

    si(N=1000, beta=0.3, gamma=0.05, days=100,
            I0=1, S0=999,
            output_filename="si_example.png")

    sir(N=1000, beta=0.2, gamma=0.1, days=200,
            I0=1, S0=999, R0=0,
            output_filename="mild_epidemic.png")

    sir(N=1000, beta=0.5, gamma=0.05, days=200,
            I0=1, S0=999, R0=0,
            output_filename="severe_epidemic.png")

    print(f"\nAll done in {time.time() - t_all:.2f}s")

if __name__ == "__main__":
    plot()