# SIR-model Figurgenerator

Denne script genererer epidemiologiske modelgrafer til brug som figurer i mit SRP 

## Modeller

### SimpleSI-model
En basal model med to tilstande og ingen restituering:
- **S** – Modtagelige (*Susceptible*)
- **I** – Inficerede (*Infected*)

### SI-model
En udvidet SI-model med to tilstande:
- **S** – Modtagelige (*Susceptible*)
- **I** – Inficerede (*Infected*)

### SIR-model
En model med tre tilstande:
- **S** – Modtagelige (*Susceptible*)
- **I** – Inficerede (*Infected*)
- **R** – Fjernede/Døde (*Removed*)

### SIRDemography-model
En SIR-model med demografi (fødsler og dødsfald):
- **S** – Modtagelige (*Susceptible*)
- **I** – Inficerede (*Infected*)
- **R** – Fjernede/Døde (*Removed*)


## Brug

```python
from models import SI, SIR, SIRDemography


def plot():
    SI(N=1000, beta=0.3, gamma=0.1, I0=1,
        S0=999).run(days=100, showRe=True,
        output="si_example.png")


    SIR(N=1000, beta=0.5, gamma=0.05, I0=1,
        S0=999, R0=0).run(days=200, showRe=True,
        output="sir_epidemic.png")


    SIRDemography(N=1000, Alpha=10, beta=0.3, gamma=0.1,
        mu=0.01, I0=1, S0=999, R0=0).run(days=300, showRe=True,
        output="sir_demography_example.png")

if __name__ == "__main__":
    plot()
```

Kør direkte med:

```bash
python example.py
```

Graferne gemmes som `.png`-filer i den samme mappe, scriptet køres fra.


## Krav

```
numpy
scipy
matplotlib
```
