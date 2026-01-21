from django.contrib import admin

# Register your models here.
from .models import User, OTP, FormSubmission

admin.site.register(User)
admin.site.register(OTP)
admin.site.register(FormSubmission)
