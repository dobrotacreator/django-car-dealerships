from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserSerializer
from .services import RegistrationLogic, PasswordLogic, ChangeUsernameEmailLogic


class AuthorizationViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return RegistrationLogic.send_activation_email(request, user)

    @action(detail=False, methods=['get'])
    def activate(self, request):
        token = request.GET.get('token')
        uid = request.GET.get('uid')

        return RegistrationLogic.activate_account(token, uid)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        return PasswordLogic.change_password(request, old_password, new_password)

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        email = request.data.get('email')

        return PasswordLogic.reset_password(request, email)

    @action(detail=False, methods=['get'])
    def reset_password_confirm(self, request):
        token = request.GET.get('token')
        uid = request.GET.get('uid')

        return PasswordLogic.reset_password_confirm(request, token, uid)

    @action(detail=False, methods=['post'])
    def reset_password_confirm(self, request):
        token = request.POST.get('token')
        uid = request.POST.get('uid')

        return PasswordLogic.reset_password_confirm(request, token, uid)

    @action(detail=False, methods=['post'])
    def change_username_email(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        return ChangeUsernameEmailLogic.change_username_email(request, password, username, email)
