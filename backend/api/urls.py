from django.urls import path
from .views import send_otp, verify_otp, submit_form, my_data

urlpatterns = [
    path("auth/send-otp/", send_otp),
    path("auth/verify-otp/", verify_otp),
    path("form/submit/", submit_form),
    path("form/my-data/", my_data),
]
