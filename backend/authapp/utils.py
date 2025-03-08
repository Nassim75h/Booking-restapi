from rest_framework_simplejwt.tokens import AccessToken
from datetime import timedelta
from django.conf import settings

from authapp.models import User


def send_activation_email(request, user):
    from authapp.email import ActivationEmail
    try:
        email = ActivationEmail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            request=request,
            context={"user": user},
        )
        email.send(user.email)
    except Exception as e:
        print(f"Failed to send activation email: {e}")
     #    logger.error(f"Failed to send activation email: {e}")


def send_reset_password_email(request, user):
    from authapp.email import SendPasswordResetEmail
    try:
        email = SendPasswordResetEmail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            request=request,
            context={"user": user},
        )
        email.send(user.email)
    except Exception as e:
        print(f"Failed to send reset password email: {e}")
     #    logger.error(f"Failed to send activation email: {e}")


def make_token(user):
    """
    Generate a token using SimpleJWT , we can use short token instead
    will use in in every functionality needed to authenticate 
    """
    token = AccessToken()
    token["user_id"] = user.id
    token.set_exp(lifetime=timedelta(minutes=15))
    return str(token)


def get_user_from_token(token):
    """Get user based on the token."""
    try:
        decoded_token = AccessToken(token)
        user_id = decoded_token.get("user_id")
        return User.objects.get(id=user_id)

    except (ValueError, User.DoesNotExist):
        raise ValueError("Invalid or expired reset token!!")
