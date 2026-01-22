import random
from django.utils import timezone
from datetime import timedelta


def generate_otp():
    return str(random.randint(100000, 999999))


def get_expiry_time():
    return timezone.now() + timedelta(minutes=5)


def validate_resume(file):
    allowed_types = ['application/pdf']
    if file.content_type not in allowed_types:
        return False, "Resume must be a PDF file"
    if file.size > 5 * 1024 * 1024:
        return False, "Resume size must be under 5MB"
    return True, None


def validate_image(file):
    allowed_types = ['image/jpeg', 'image/png']
    if file.content_type not in allowed_types:
        return False, "Image must be JPG or PNG"
    if file.size > 5 * 1024 * 1024:
        return False, "Image size must be under 5MB"
    return True, None
