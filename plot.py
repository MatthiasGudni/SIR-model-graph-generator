import time
from models import simple_si, si, sir, sir_demography

def plot():
    t_all = time.time()

    simple_si(N=1000, beta=0.3, days=50,
            I0=1, S0=999,
            output_filename="simple_si_example.png")

    si(N=1000, beta=0.3, gamma=0.05, days=100,
            I0=1, S0=999,
            output_filename="si_example.png")

    sir(N=1000, beta=0.3, gamma=0.1, days=200,
            I0=1, S0=999, R0=0, showRe=True,
            output_filename="mild_epidemic.png")

    sir(N=1000, beta=0.5, gamma=0.05, days=200,
            I0=1, S0=999, R0=0,
            output_filename="severe_epidemic.png")
    
    sir_demography(N=1000, Alpha=10, beta=0.3, gamma=0.1, mu=0.01, days=300,
                   I0=1, S0=999, R0=0,
                   output_filename="sir_demography_example.png")

    print(f"\nAll done in {time.time() - t_all:.2f}s")

if __name__ == "__main__":
    plot()