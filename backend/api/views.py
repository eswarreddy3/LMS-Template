from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import User, OTP, FormSubmission
from .serializers import FormSubmissionSerializer
from .utils import generate_otp, get_expiry_time

from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    email = request.data.get("email")
    phone = request.data.get("phone")

    if not email and not phone:
        return Response({"error": "Email or phone required"}, status=400)

    user, created = User.objects.get_or_create(
        email=email if email else None,
        phone=phone if phone else None
    )

    otp_code = generate_otp()
    expiry = get_expiry_time()

    OTP.objects.create(user=user, otp=otp_code, expires_at=expiry)

    # TODO: Send OTP via Email/SMS
    print("OTP:", otp_code)  # For testing

    return Response({"message": "OTP sent successfully"})


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    email = request.data.get("email")
    phone = request.data.get("phone")
    otp_input = request.data.get("otp")

    try:
        user = User.objects.get(email=email) if email else User.objects.get(phone=phone)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    otp_obj = OTP.objects.filter(user=user, otp=otp_input).last()

    if not otp_obj:
        return Response({"error": "Invalid OTP"}, status=400)

    if otp_obj.expires_at < timezone.now():
        return Response({"error": "OTP expired"}, status=400)

    user.is_verified = True
    user.save()

    refresh = RefreshToken.for_user(user)

    return Response({
        "message": "Login successful",
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_form(request):
    serializer = FormSubmissionSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_data(request):
    data = FormSubmission.objects.filter(user=request.user)
    serializer = FormSubmissionSerializer(data, many=True)
    return Response(serializer.data)
