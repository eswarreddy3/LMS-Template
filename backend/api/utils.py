import random
from django.utils import timezone
from datetime import timedelta


def generate_otp():
    return str(random.randint(100000, 999999))


def get_expiry_time():
    return timezone.now() + timedelta(minutes=5)
