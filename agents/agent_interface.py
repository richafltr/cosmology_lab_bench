"""Abstract interface for agents operating inside the Cosmology Lab Bench."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseCosmologyAgent(ABC):
    """Abstract agent for cosmological hypothesis testing and research orchestration."""

    def __init__(self, name: str = "BaseAgent"):
        self.name = name

    @abstractmethod
    def act(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """Given current laboratory observation, choose next tool action to execute."""
        pass
