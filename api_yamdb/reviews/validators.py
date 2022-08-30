from django.core.exceptions import ValidationError
import datetime as dt


def validate_year(value):
    year = dt.date.today().year
    if (value > year):
        raise ValidationError('Проверьте год выпуска!')
    return value
