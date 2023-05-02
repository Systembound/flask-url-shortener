from marshmallow import ValidationError


def validate_url_length(url):
    if len(url) > 2040:
        raise ValidationError('URL must not exceed 2040 characters.')
