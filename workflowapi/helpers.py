from django.core.exceptions import ValidationError


def validate_input_dictionary(workflow_input_list: list, request_input_dictionary: dict):
    for key in request_input_dictionary.keys():
        if key not in workflow_input_list:
            raise ValidationError(message="Inputs don't match")
