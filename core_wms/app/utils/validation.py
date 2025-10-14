from typing import TypeVar
from pydantic import TypeAdapter, BaseModel

T = TypeVar("T", bound=BaseModel)


def validate_list(model_class: type[T], data: list) -> list[T]:
    """
    Validate a list of objects using Pydantic TypeAdapter.

    Args:
        model_class: The Pydantic model class to validate against
        data: List of objects to validate

    Returns:
        List of validated model instances

    Example:
        suppliers = validate_list(Supplier, stmt)
    """
    return TypeAdapter(list[model_class]).validate_python(data)


def validate_single(model_class: type[T], data) -> T:
    """
    Validate a single object using Pydantic model validation.

    Args:
        model_class: The Pydantic model class to validate against
        data: Object to validate

    Returns:
        Validated model instance

    Example:
        supplier = validate_single(Supplier, stmt)
    """
    return model_class.model_validate(data)
