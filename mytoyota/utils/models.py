"""Utilities for manipulating or extend pydantic models."""
from pydantic.v1 import BaseModel, root_validator


class CustomBaseModel(BaseModel):
    """Model that automatically returns values that cannot be parsed correctly as 'None' value."""

    @root_validator(pre=True)
    def invalid_to_none(cls, values: dict[str, object]) -> dict[str, object]:  # noqa: N805
        """Pydantic Root validator parsing config."""
        validated_values: dict[str, object] = {}
        for name, value in values.items():
            field = cls.__fields__.get(name)
            if field is None:  # must be extra data
                continue
            validated_value, errors = field.validate(
                value,
                validated_values,
                loc="__root__",
                cls=cls,  # type: ignore[arg-type]
            )
            validated_values[name] = validated_value
            if errors:
                values[name] = None
        return values
