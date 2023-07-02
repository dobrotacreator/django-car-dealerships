from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from .models import User


class RegistrationLogic:
    @staticmethod
    def send_activation_email(request, user: User) -> Response:
        """
        Register a new user and send an activation email.

        Args:
            request: The HTTP request object.
            user: The instance of user for registration.

        Returns: A Response object indicating the result of the registration process.

        Raises: -
        """
        token = default_token_generator.make_token(user)

        # Build activation URL
        current_site = get_current_site(request)
        protocol = 'https' if request.is_secure() else 'http'
        activation_url = f'{protocol}://{current_site.domain}{reverse("activate")}' \
                         f'?uid={user.id}&token={token}'

        # Create activation email message
        mail_subject = 'Activate your account'
        message = f'Hello {user.username},\n\nPlease click the link below to activate your account:\n\n{activation_url}'

        # Send confirmation email
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return Response({'detail': 'Account created. Please check your email to activate your account.'},
                        status=status.HTTP_201_CREATED)

    @staticmethod
    def activate_account(token: str, uid: int) -> Response:
        """
        Activate a user account based on the provided activation token and user ID.

        Args:
            token: The activation token.
            uid: The user ID.

        Returns: A Response object indicating the result of the account activation.

        Raises: -
        """
        try:
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'detail': 'Account activated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordLogic:
    @staticmethod
    def change_password(request, old_password: str, new_password: str) -> Response:
        """
        Change the user's password based on the provided old and new passwords.

        Args:
            request: The HTTP request object.
            old_password: The old password.
            new_password: The new password.

        Returns: A Response object indicating the result of the password change.

        Raises: -
        """
        user = request.user

        if not user.check_password(old_password):
            return Response({'detail': 'Invalid old password.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)

    @staticmethod
    def reset_password(request, email: str) -> Response:
        """
        Reset the user's password and send a password reset email.

        Args:
            request: The HTTP request object.
            email: The email address associated with the user.

        Returns: A Response object indicating the result of the password reset process.

        Raises: -
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Generate password reset token
        token = default_token_generator.make_token(user)

        # Build password reset URL
        current_site = get_current_site(request)
        protocol = 'https' if request.is_secure() else 'http'
        reset_url = f'{protocol}://{current_site.domain}{reverse("reset_password_confirm")}' \
                    f'?uid={user.id}&token={token}'

        # Create password reset email message
        mail_subject = 'Reset your password'
        message = f'Hello {user.username},\n\nPlease click the link below to reset your password:\n\n{reset_url}'

        # Send password reset email
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return Response({'detail': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)

    @staticmethod
    def reset_password_confirm(request, token: str, uid: int) -> Response:
        """
        Handle the password reset confirmation and reset the user's password.

        Args:
            request: The HTTP request object.
            token: The password reset token.
            uid: The user ID.

        Returns: A Response object indicating the result of the password reset confirmation.

        Raises: -
        """
        try:
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid password reset link.'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            if request.method == 'GET':
                # Allow the user to reset the password
                return Response({'detail': 'Please reset your password.'}, status=status.HTTP_200_OK)
            elif request.method == 'POST':
                password = request.data.get('password')
                # Reset the user's password
                user.set_password(password)
                user.save()

                return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid password reset link.'}, status=status.HTTP_400_BAD_REQUEST)


class ChangeUsernameEmailLogic:
    @staticmethod
    def change_username_email(request, password: str, username: str = None, email: str = None) -> Response:
        """
        Change the user's username and/or email.

        Args:
            request: The HTTP request object.
            password: The user's current password for verification.
            username: The new username (optional).
            email: The new email (optional).

        Returns: A Response object indicating the result of the username/email change.

        Raises: -
        """
        user = request.user

        if not user.check_password(password):
            return Response({'detail': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)

        if username:
            user.username = username
        if email:
            user.email = email

        user.save()

        return Response({'detail': 'Username/Email changed successfully.'}, status=status.HTTP_200_OK)
