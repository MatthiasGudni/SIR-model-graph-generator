from abc import ABC, abstractmethod
from .solver import run_model as _solve


class CompartmentalModel(ABC):
    """Abstract base class for all compartmental epidemic models.

    Subclasses must implement _build(), returning a dict of keyword
    arguments that will be forwarded to the internal ODE solver.
    """

    @abstractmethod
    def _build(self) -> dict:
        """Return kwargs to pass to the internal solver."""
        ...

    def run(self, days=100, showRe=False, output="model.png"):
        """Solve and plot this model."""
        _solve(**self._build(), days=days, showRe=showRe, output=output)