from django.core.exceptions import ValidationError


def validate_background_image_size(file):
    max_size_kb = 500
    
    if file.size > max_size_kb * 1024:
        raise ValidationError(f'Background image cannot be larger than {max_size_kb}kb')