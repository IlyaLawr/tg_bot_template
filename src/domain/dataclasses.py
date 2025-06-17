from dataclasses import dataclass


@dataclass
class ValidationResult:
    valid: bool
    error: str | None = None
