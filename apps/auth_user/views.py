from django.db import IntegrityError
from rest_framework import renderers, parsers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth_user.serializers import (
    RegistrationSerializer
)
from apps.auth_user.services_view import (
    create_user_and_send_email_for_activation,
    activate_user_and_create_user_profile,
)


class RegistrationView(APIView):
    """APIView для регистрации пользователя"""

    renderer_classes = (renderers.JSONRenderer,)
    parser_classes = (parsers.FormParser, parsers.JSONParser)

    def get(self, request):
        return Response(template_name='auth/sign_up.html')

    def post(self, request):
        try:
            if request.data['password'] == request.data['repeat_password']:
                serializer = RegistrationSerializer(data=request.data)
                if serializer.is_valid():
                    try:
                        create_user_and_send_email_for_activation(data=serializer.data, request=request)
                    except IntegrityError:
                        return Response(data={'error': 'User with this username already exist, try again'})
                    else:
                        return Response(data={'ok': 'Check your mail'},
                                        status=status.HTTP_200_OK)
                else:
                    return Response(data=serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response(data={'error': 'Password is not equal repeat password'},
                            status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response(data={'error': 'Password or repeat password is missing!'})


class ActivationView(APIView):
    """View для активации пользователя и
    создания """

    def get(self, request, uid, token):
        print(1)
        if activate_user_and_create_user_profile(uid=uid, token=token):
            return Response(data={'ok': 'User has been activate'},
                            status=status.HTTP_200_OK)
        return Response(data={'error': 'Un valid uid or token'},
                        status=status.HTTP_400_BAD_REQUEST)
