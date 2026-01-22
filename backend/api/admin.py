from django.contrib import admin

# Register your models here.
from .models import OTP, FormSubmission

admin.site.register(OTP)
admin.site.register(FormSubmission)
