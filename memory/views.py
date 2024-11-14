from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .admin import MemoryAdmin
from .serializers import UserSerializer, ProfilePicSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Memory, ProfilePic
from .serializers import MemorySerializers
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

@api_view(['POST'])
def login(request):
    data = request.data
    username = data.get("username")
    password = data.get("password")

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)

        token, created = Token.objects.get_or_create(user=request.user)

        return Response(
            {
                "success":"Login Successfully",
                "token":token.key
            },status=status.HTTP_201_CREATED
        )

    else:
        return Response({"error":"Babe! you forgot your credentials ?"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@login_required()
@permission_classes([IsAuthenticated])
def send_image(request):
    data = request.data
    media = request.FILES.get('media')
    desc = data.get('description')

    try:

        if not request.user.is_authenticated:
            return Response(
                {"error": "Baby log in before you create a memory entry."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        image_entry = Memory.objects.create(user=request.user, media=media, description=desc)
        serializer = MemorySerializers(image_entry)

        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error":f"Error creating Memory entry: {e}"})


@api_view(['GET'])
@login_required()
@permission_classes([IsAuthenticated])
def home_page(request):
    Images = Memory.objects.filter(user=request.user)
    serializer = MemorySerializers(Images, many=True)

    return Response({"data":serializer.data}, status=status.HTTP_200_OK)



@api_view(['POST'])
def send_email(request):
    email = request.data.get("email")

    user = User.objects.filter(email=email).first()

    try:
        if user:

            reset_token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            context = {
                'reset_url': f'https://gordenarcher.pythonanywhere.com/api/reset-password/{uid}/{reset_token}',
                'username': user.username,
                'message': "Babe, you forgot your password? No problem,"
            }

            html_message = render_to_string('change_password_email.html', context)
            plain_message = strip_tags(html_message)
            subject = "Reset Password"
            from_email = "archergorden@gmail.com"
            recipient_list = [email]

            email_message = EmailMessage(subject, html_message, from_email, recipient_list)
            email_message.content_subtype = "html"
            email_message.send()

            return Response({"success": "Email sent successfully."}, status=status.HTTP_200_OK)

        else:
            return Response({"error": f"'{email}' is not a user"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": f"Error sending email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'GET':

            return Response({
                "message": "Token is valid. Please provide a new password."
            }, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            password = request.data.get("password")
            if not password:
                return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.save()

            token, created = Token.objects.get_or_create(user=user)

            # Return the new token and user data
            return Response({
                "message": "Password reset successful.",
                "token": token.key
            }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Something occurred: {str(e)}. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['GET'])
def get_user(request):
    user = request.user

    serializer = UserSerializer(user)
    return Response({"data":serializer.data}, status=status.HTTP_200_OK)




@api_view(['POST'])
@login_required()
@permission_classes([IsAuthenticated])
def set_profil_pic(request):
    user = request.user
    image = request.FILES.get('profile_image')

    if image:

        try:
            existing_image = ProfilePic.objects.get(user=user)

            existing_image.profile_image.delete()
            existing_image.delete()

        except ProfilePic.DoesNotExist:
            pass

        new_image = ProfilePic.objects.create(user=user, profile_image=image)
        return Response({"message": "Profile image updated successfully."}, status=status.HTTP_200_OK)

    return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_required()
@permission_classes([IsAuthenticated])
def get_profilepic(request):
    user = request.user

    try:

        image_entry = ProfilePic.objects.get(user=user)
        serializer = ProfilePicSerializer(image_entry)

        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)


    except ProfilePic.DoesNotExist:

        return Response({"error": "Profile picture not found."}, status=status.HTTP_404_NOT_FOUND)


    except Exception as e:

        return Response({"error": f"Error retrieving profile picture: {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_image(request, pk):
    user = request.user

    try:
        memory_entry = Memory.objects.get(pk=pk, user=user)
        memory_entry.delete()

        return Response({"data": "Memory image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except ObjectDoesNotExist:
        return Response({"error": "Memory with this id does not exist or is not related to the authenticated user"},
                        status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)