from os import stat
from django.core.exceptions import ValidationError
import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime,timedelta
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken


from authapp.utils import get_user_from_token, send_activation_email
from .models import Profile, User
from .serializers import (
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    ProfileSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)



class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_activation_email(request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh =RefreshToken.for_user(user)
        return Response(
            {"refresh": str(refresh), 
            "access": str(refresh.access_token)},
            status=status.HTTP_200_OK)
       
class RefreshAccessToken(APIView):
    
    def post(self,request):
        refresh_token = request.data.get('refresh')

        if not refresh_token :
            return Response({"error":"RefreshToken is Required"},status=status.HTTP_401_UNAUTHORIZED)
        try :
            decoded = jwt.decode(refresh_token,settings.SECRET_KEY,algorithms=['HS256'])
        except jwt.ExpiredSignatureError :
            return Response ({"error ": "Token is expired "},status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError :
            return Response({"error" :"Invalid token"},status=status.HTTP_401_UNAUTHORIZED)

        user_id = decoded['user_id']
        refresh_expire = datetime.utcfromtimestamp(decoded['exp'])
        token_time_threshold = 5
        if refresh_expire < datetime.utcnow() + timedelta(minutes=token_time_threshold):

            try :
                new_refresh=RefreshToken()
                new_refresh.payload['user_id'] = user_id
                access=new_refresh.access_token
                return Response({"access":str(access),"refresh":str(new_refresh)},status=status.HTTP_200_OK)

            except Exception as e:
                return Response ({"error":f"Error while creating new refresh token {str(e)}"},status=status.HTTP_401_UNAUTHORIZED)
        else :
            try :
                refresh= RefreshToken(refresh_token)
                new_access = refresh.access_token
                return Response(
                    {"access":str(new_access)},
                    status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error" :f"Error while  refreshing the token {str(e)}"},status=status.HTTP_401_UNAUTHORIZED)

 
    
class ProfileView(ModelViewSet):
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # NOTE  : fetch  authenticated user
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    # TODO: we need to change the implementation of signals if we intend creting a user_profile only if user_acc is activated
    def get_object(self):
        profile = Profile.objects.get(user=self.request.user)
        return profile


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    # NOTE: YACINE : you can pass user directly in context serializer since user is authenticated
    # context={"user": self.request.user}

    def patch(self, validated_data):
        serializer = ChangePasswordSerializer(
            data=self.request.data, context={"user": self.request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password changes successfully"}, status=status.HTTP_200_OK)


# TODO : add the functioning of sending and email
class SendPasswordResetEmailView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(
                {"message": "A password reset email has been sent.Please check your inbox and spam folder!"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO remove this get request since its just for testing purpose also make sure to remove it from verification_via_email/urls
class TempValidateRequestResetPassLink(APIView):
    def get(self, request, token, *args, **kwargs):
        if not token:
            return Response({"error": "Token  is required!!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_from_token(token)
            if not user:
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Token is valid."}, status=status.HTTP_200_OK)
        except (User.DoesNotExist, ValueError):
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """
    Handle reset password .
    """

    def post(self, request, *args, **kwargs):
        """
        Reset the password using the token
        """
        serializer = PasswordResetSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # reset the password
        return Response({"message": "Password has been successfully reset."}, 
                        status=status.HTTP_200_OK)



class ActivateAccountView(APIView):
    def get(self,request,token=None,*args,**kwargs):

        if token == None :
            token = kwargs.get('token',None)

        if not token :
            return Response({"error":"Invalid token"},
                            status=status.HTTP_400_BAD_REQUEST)
                   
        try:
            decoded_token = AccessToken(token)
            user_id = decoded_token.get("user_id")
            user = User.objects.get(id=user_id)
            if user.is_active :
                return Response({"message":"Account already activated"},status=status.HTTP_403_FORBIDDEN)
            user.is_active = True
            user.save()
            refresh=RefreshToken()
            refresh.payload['user_id']=user_id
            access=refresh.access_token

            return Response({"message": "Account activated successfully!",
                             "refresh":str(refresh),
                             "access":str(access)}, 
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Invalid or expired token, {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)







