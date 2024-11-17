from enum import Enum


class Ambient(Enum):
    """Enum class to define the ambient as production or sandbox(development)."""

    SANDBOX = "SANDBOX"  # for development and tests
    PRODUCTION = "PRODUCTION"
