import json
import requests

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.urls import reverse

from rest_framework.authtoken.models import Token

from apps.auth_user.models import Uid
from social_network import settings


def create_user_and_send_email_for_activation(data: dict, request) -> None:
    """Создание пользователя и отправка
    письма на почту для активации"""

    user = get_user_model().objects.create(username=data['username'],
                                           password=make_password(data['password']),
                                           email=data['email'],
                                           last_name=data['last_name'],
                                           first_name=data['first_name'],
                                           is_active=False)
    new_data = _create_unique_uid_and_token(user=user)
    url = _get_web_url(is_secure=request.is_secure(),
                       host=request.get_host(),
                       url=f'/auth/activation/{new_data["uid"]}/{new_data["token"]}/')
    send_mail(subject='Activation mail',
              message=f'Your activation link: \n {url}',
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[data['email']],
              fail_silently=False)


def activate_user_and_create_user_profile(uid: str, token: str) -> bool:
    """Активация пользователя и создание профиля пользователя"""

    if _verification_uid_and_token(uid=uid, token=token):
        verification_data = _get_verification_data_or_404(
            uid=uid,
            token=token
        )
        new_user = verification_data['uid_object'].user
        new_user.is_active = True
        new_user.last_login = timezone.now()
        new_user.save()
        _delete_uid_and_token(uid_object=verification_data['uid_object'],
                              token_object=verification_data['token_object'])
        return True
    else:
        return False


def log_in(request, data: dict) -> dict:
    """Check password and return tokens or false"""

    try:
        user = get_user_model().objects.get(username=data['username'])
        if check_password(data['password'], user.password):
            url = _get_web_url(
                is_secure=request.is_secure(),
                host=request.get_host(),
                url=reverse('token')
            )
            response = requests.post(url=url, json={
                'password': data['password'],
                'username': user.username
            })
            data = json.loads(response._content.decode('utf-8'))
            data.update({'user_id': user.id})
            return data
        return {'error': 'Invalid password'}
    except Exception:
        return {'error': 'User does not exist'}


def reset_password(request, data: dict) -> dict:
    """Send email for reset password"""

    try:
        user = get_user_model().objects.get(email=data['email'])
    except Exception:
        return {'error': 'User does not exist'}
    else:
        new_data = _create_unique_uid_and_token(user=user)
        url = _get_web_url(is_secure=request.is_secure(),
                           host=request.get_host(),
                           url=f'/auth/reset_password/{new_data["uid"]}/{new_data["token"]}/')
        send_mail(subject='Reset password mail',
                  message=f'Your reset password link: \n {url}',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[data['email']],
                  fail_silently=False)


def set_password(uid: str, token: str, data: dict) -> None:
    """Set new password after confirm"""

    verification_data = _get_verification_data_or_404(
        uid=uid,
        token=token
    )

    verification_data['token_object'].user.password = make_password(data['password'])
    verification_data['token_object'].user.save()
    _delete_uid_and_token(uid_object=verification_data['uid_object'],
                          token_object=verification_data['token_object'])


def _create_unique_uid_and_token(user) -> dict:
    """Создание уникального юида и токена
    для потдверждения уникальности пользователя"""

    uid = Uid.objects.create(user=user)
    token = Token.objects.create(user=user)
    return {
        'uid': uid.uid,
        'token': token.key
    }


def _delete_uid_and_token(uid_object, token_object) -> None:
    """Удаление объектов юида и токена"""

    uid_object.delete()
    token_object.delete()


def _verification_uid_and_token(uid: str, token: str) -> bool:
    """Проверка юида и токена на правильность"""

    verification_data = _get_verification_data_or_404(
        uid=uid,
        token=token
    )

    if verification_data['token_object'].user == verification_data['uid_object'].user:
        return True
    return False


def _get_verification_data_or_404(uid: str, token: str) -> dict:
    """Получение объектов юида и токена"""

    uid_object = get_object_or_404(klass=Uid,
                                   uid=uid)
    token_object = get_object_or_404(klass=Token,
                                     key=token)
    return {
        'uid_object': uid_object,
        'token_object': token_object
    }


def _get_web_url(is_secure: bool, host: str, url: str) -> str:
    """Получение ссылки"""

    protocol = 'https://' if is_secure else 'http://'
    web_url = protocol + host
    return web_url + url
