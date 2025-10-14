from graphql import ValidationRule, GraphQLError

class EnumValidationRule(ValidationRule):
    """General class for an enum validation rule

    Simple functionality, needs iteration in the near future.
    """

    ENUM_FIELDS = {'currency': ['EUR']}
    
    def enter_argument(self, node, *args) -> None:
        if node.name.value in self.ENUM_FIELDS:
            valid_values = self.ENUM_FIELDS[node.name.value]
            provided_value = getattr(node.value, 'value', None)
            
            if provided_value and provided_value not in valid_values:
                self.report_error(GraphQLError(
                    f"Invalid value '{provided_value}' for '{node.name.value}'. "
                    f"Must be one of: {', '.join(sorted(valid_values))}"
                ))