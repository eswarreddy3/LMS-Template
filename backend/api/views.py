from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.utils import timezone
from .models import User, OTP, FormSubmission
from .serializers import FormSubmissionSerializer
from .utils import generate_otp, get_expiry_time
from django.contrib.auth.models import User
import cloudinary.uploader
from .utils import validate_resume, validate_image


@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    email = request.data.get("email")
    phone = request.data.get("phone")

    if not email and not phone:
        return Response({"error": "Email or phone required"}, status=400)

    user, created = User.objects.get_or_create(username=email, email=email)


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
    name = request.data.get("name")
    age = request.data.get("age")
    resume = request.FILES.get("resume")
    image = request.FILES.get("image")

    if not all([name, age, resume, image]):
        return Response({"error": "All fields are required"}, status=400)

    is_valid_resume, resume_error = validate_resume(resume)
    if not is_valid_resume:
        return Response({"error": resume_error}, status=400)

    is_valid_image, image_error = validate_image(image)
    if not is_valid_image:
        return Response({"error": image_error}, status=400)

    resume_upload = cloudinary.uploader.upload(resume, resource_type="raw")
    image_upload = cloudinary.uploader.upload(image, resource_type="image")

    form = FormSubmission.objects.create(
        user=request.user,
        name=name,
        age=age,
        resume_url=resume_upload["secure_url"],
        image_url=image_upload["secure_url"]
    )

    return Response({
        "message": "Form submitted successfully",
        "data": {
            "id": form.id,
            "name": form.name,
            "age": form.age,
            "resume_url": form.resume_url,
            "image_url": form.image_url,
        }
    }, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_data(request):
    submissions = FormSubmission.objects.filter(user=request.user).order_by('-created_at')
    serializer = FormSubmissionSerializer(submissions, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_submission(request, pk):
    try:
        submission = FormSubmission.objects.get(pk=pk, user=request.user)
    except FormSubmission.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    # Extract Cloudinary public IDs
    resume_url = submission.resume_url
    image_url = submission.image_url

    def get_public_id(url):
        return url.split('/')[-1].split('.')[0]

    resume_public_id = get_public_id(resume_url)
    image_public_id = get_public_id(image_url)

    # Delete from Cloudinary
    cloudinary.uploader.destroy(resume_public_id, resource_type="raw")
    cloudinary.uploader.destroy(image_public_id, resource_type="image")

    # Delete DB record
    submission.delete()

    return Response({"message": "Submission deleted successfully"})
