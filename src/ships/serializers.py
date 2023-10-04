from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exception, context):
    if isinstance(exception, DjangoValidationError):
        detail = exception.message_dict if hasattr(exception, 'message_dict') else exception.message
        exception = ValidationError(detail=detail)

    return drf_exception_handler(exception, context)
