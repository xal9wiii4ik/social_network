from django.db import IntegrityError

from rest_framework import renderers, parsers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth_user.serializers import (
    RegistrationSerializer,
    LogInSerializer,
    ResetPasswordSerializer,
    SetPasswordSerializer,
)
from apps.auth_user.services_view import (
    create_user_and_send_email_for_activation,
    activate_user_and_create_user_profile,
    log_in,
    reset_password,
    set_password, _verification_uid_and_token,
)


class RegistrationView(APIView):
    """APIView для регистрации пользователя"""

    renderer_classes = (renderers.JSONRenderer,)
    parser_classes = (parsers.FormParser, parsers.JSONParser)

    def get(self, request):
        return Response(template_name='auth/sign_up.html')

    def post(self, request):

        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data['password'] == serializer.data['repeat_password']:
                try:
                    create_user_and_send_email_for_activation(data=serializer.data, request=request)
                except IntegrityError:
                    return Response(data={'error': 'User with this username already exist, try again'})
                else:
                    return Response(data={'ok': 'Check your mail'},
                                    status=status.HTTP_200_OK)
            else:
                return Response(data={'error': 'Password and repeat password is not equal'})
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    """View для активации пользователя и
    создания """

    def get(self, request, uid, token):
        if activate_user_and_create_user_profile(uid=uid, token=token):
            return Response(data={'ok': 'User has been activate'},
                            status=status.HTTP_200_OK)
        return Response(data={'error': 'Un valid uid or token'},
                        status=status.HTTP_400_BAD_REQUEST)


class LogInView(APIView):
    """View for login and take token"""

    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        if serializer.is_valid():
            data = log_in(request=request, data=serializer.data)
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """View for resetting user's password before set password"""

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            data = reset_password(request=request, data=serializer.data)
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(APIView):
    """View for set new password"""

    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer,)
    parser_classes = (parsers.FormParser, parsers.JSONParser)

    def get(self, request, uid, token):
        if _verification_uid_and_token(uid=uid, token=token):
            return Response(data={'uid': uid, 'token': token},
                            status=status.HTTP_200_OK,
                            template_name='set_password.html')
        return Response(data={'error': 'Un valid uid or token'},
                        status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uid: str, token: str):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data['password'] == serializer.data['repeat_password']:
                set_password(uid=uid, token=token, data=serializer.data)
                return Response(data={'ok': 'The password was changed'}, status=status.HTTP_200_OK)
            else:
                return Response(data={'error': 'Password and repeat password is not equal'})
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
