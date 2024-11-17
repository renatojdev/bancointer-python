from enum import Enum


class Environment(Enum):
    """Enum class to define the environment as production or sandbox(development)."""

    SANDBOX = "SANDBOX"  # for development and tests
    PRODUCTION = "PRODUCTION"

    def get_environment_by_value(value):
        for env in Environment:
            if env.value == value:
                return env
        return None