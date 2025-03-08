from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import AccessToken
from .utils import get_user_from_token, send_reset_password_email
from .models import Profile, User


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username","first_name","last_name", "password",
                  "confirm_password", "terms_cond"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError("Passwords dont match")

        try:
            # validate passowrd used django validators
            validate_password(password)
        except ValidationError as e:
            # re-raise errors associated with password field
            raise serializers.ValidationError({"password": e.messages})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        # Note: we make our custom authenticate method since the built-in authenticate one do authentication for only activate user is_active=True , but we have to do the activation vai email so default one would be false
        attrs["user"] = self.authenticate(email, password)

        return attrs

    def authenticate(self, email, password):
        try:
            user = User.objects.get(email=email.lower())
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"non_field_errors": "There is no user with that email. Signup"})

        # check if the user is active
        if not user.is_active:
            raise serializers.ValidationError(
                {"non_field_errors": 
                    "Account is not active. check your email and activate your account"}
            )

        # verify the password
        if not check_password(password, user.password):
            raise serializers.ValidationError(
                {"non_field_errors": "Invalid password!!"}
            )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=127)

    class Meta:
        model = Profile
        fields = ['id',"user_id", "username", "first_name",
                  "last_name", "age", "languages", "location"]

    # NOTE : fixed :)
    def save(self, **kwargs):
        username = self.validated_data.get('username')
        if username:
            if Profile.objects.filter(username=username).exclude(id=self.instance.id).exists():
                raise ValidationError({"message": "user name taken"})

        profile = super().save(**kwargs)
        return profile


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20, write_only=True)
    new_password = serializers.CharField(max_length=20, write_only=True)
    confirm_password = serializers.CharField(max_length=20, write_only=True)

    def validate(self, attrs):
        user = self.context['user']

        if not user.check_password(attrs['password']):
            raise serializers.ValidationError(
                {"message": "password is incorrect"})
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"message": "passwords dont match"})

        return attrs

    def save(self, **kwargs):
        user = self.context['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=127, required=False)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        request = self.context.get('request')
        # NOTE :aprroved :)_
        if not bool(username) ^ bool(email):  # XOR ;) => 0,0 - 1,1 means 1
            raise serializers.ValidationError(
                "You must give exactly one of 'username' or 'email', not both or neither!!"
            )
        if not request:
            raise ValueError("Request object must be in context serializer!")

        given_property = username or email
        lookup_feild = "username" if username else "email"
        try:
            user = User.objects.get(**{lookup_feild: given_property})
            # send_reset password _email
            send_reset_password_email(request, user)
            attrs['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError(
                f"No account with the given {given_property} was found")

        return attrs

class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(
        write_only=True, required=True, min_length=8)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("The new passwords don't match.")

        try:
            user = get_user_from_token(attrs['token'])
        except Exception:
            raise serializers.ValidationError(
                "Invalid or expired reset token.")

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']

        # reset password and save user
        user.set_password(new_password)
        user.save()
        return user
