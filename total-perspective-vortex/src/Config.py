from dataclasses import dataclass, FrozenInstanceError


@dataclass(frozen=True)
class Config:
    EXCEPTIONS = (
        TypeError, IndexError, FileNotFoundError,
        ValueError, AttributeError, OSError,
        KeyboardInterrupt, FrozenInstanceError,
        ImportError, AssertionError, RuntimeError
    )
