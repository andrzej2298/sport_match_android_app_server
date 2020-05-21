from rest_framework.views import exception_handler


def _get_key(response, field):
    if isinstance(response.data[field], list):
        return response.data[field][0]
    else:
        return response.data[field]


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    error_key = ''
    error_fields = []

    for field in reversed(response.data):
        if field not in ['detail', 'non_field_errors']:
            error_key = _get_key(response, field)
            error_fields = [field]

    if 'detail' in response.data:
        error_key = _get_key(response, 'detail')
    if 'non_field_errors' in response.data:
        error_key = _get_key(response, 'non_field_errors')

    if '|' in error_key:
        split = error_key.split('|')
        error_key = split[0]
        error_fields = split[1].split(', ')

    response.data = {
        'error_key': error_key,
        'error_fields': error_fields,
    }
    return response
