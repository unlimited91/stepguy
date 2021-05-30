import os
from functools import partial

from django.http import JsonResponse


def env_var(variable_name, variable_type, default=None):
    """Returns Environment Variable with `variable_name` while `variable_type` takes in a type
    to use as type cast while returning the variable value. Raises exception if it is not set (None).

    Examples:
        env_var('HELLO', str)  # export HELLO="WORLD"
        env_var('TALLY', int)  # export TALLY=23
        env_var('DEBUG', bool) # export DEBUG="True"

    For booleans, make sure you type in the full words 'True' or 'False', case is not important.
    """
    value = os.getenv(variable_name, None)

    # Hopeless situation
    if value is None and default is None:
        raise Exception('Cannot load environment variable: %s' % (variable_name))

    # Work with defaults, force through the typecast.
    if value is None:
        return variable_type(default)

    # Booleans appear as text, convert to their natural form
    if variable_type is bool:
        try:
            return {'true': True, 'false': False}[value.lower()]
        except KeyError:
            raise Exception('Boolean variable types must have values: "True" or "False", got "%s"' % (value))

    # Let Python work its magic
    return variable_type(value)


JsonOKResponse = partial(JsonResponse, status=200)
JsonCreatedResponse = partial(JsonResponse, status=201)
JsonAcceptedResponse = partial(JsonResponse, status=202, data={})
JsonNoContentResponse = partial(JsonResponse, status=204, data={})
JsonBadRequestResponse = partial(JsonResponse, status=400)
JsonNotAuthorizedResponse = partial(JsonResponse, status=401, data={})
JsonNotPermittedResponse = partial(JsonResponse, status=403, data={})
JsonNotFoundResponse = partial(JsonResponse, status=404, data={})
JsonUnprocessableEntityResponse = partial(JsonResponse, status=422)