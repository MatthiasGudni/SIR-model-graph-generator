# SIR-model Figurgenerator

Denne script genererer epidemiologiske modelgrafer til brug som figurer i mit SRP 

## Modeller

### SI-model
En simpel model med to tilstande:
- **S** – Modtagelige (*Susceptible*)
- **I** – Inficerede (*Infected*)

### SIR-model
En udvidet model med tre tilstande:
- **S** – Modtagelige (*Susceptible*)
- **I** – Inficerede (*Infected*)
- **R** – Fjernede/Døde (*Removed*)


## Brug

```python
from models import si, sir

def plot():
    si(N=1000, beta=0.3, days=100,
            I0=1, S0=999,
            output_filename="si_eksempel.png")

    sir(N=1000, beta=0.2, gamma=0.1, days=200,
            I0=1, S0=999, R0=0,
            output_filename="sir_eksempel.png")

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
