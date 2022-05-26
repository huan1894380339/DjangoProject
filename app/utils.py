from __future__ import annotations

import datetime
import os
import random
import string

import jwt
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework_simplejwt.tokens import RefreshToken
from projectnew.settings import EMAIL_HOST, REFRESH_TOKEN_SECRET, SECRET_KEY

from .models import CustomerUser


def snake_case(username, email, password, code_verify):
    to = email
    html_content = render_to_string(
        'mail.html',
        {'username': username, 'password': password, 'code_verify': code_verify},
    )
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives('subject', text_content, EMAIL_HOST, [to])
    email.attach_alternative(html_content, 'text/html')
    email.send()


def generate_access_token(user: CustomerUser):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(
        access_token_payload,
        SECRET_KEY,
        algorithm='HS256',
    )
    return access_token


def generate_refresh_token(user: CustomerUser) -> str:
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(
        refresh_token_payload,
        REFRESH_TOKEN_SECRET,
        algorithm='HS256',
    )

    return refresh_token


def get_list_path_images(path: str) -> list:
    """
    Get list path images in local
    :params:
        - path (str): The path parent in local
    :return:
        list: List path images
    """
    # Open folder by path and get list file or list folder name
    find_folder = os.listdir(path)
    list_path_file_image = dict()
    anhchinh = 'AnhChinh'  # The folder has two folder child are: Anh Chinh and Anh Phu
    for foldername in find_folder:
        if foldername in ['AnhChinh', 'AnhPhu']:
            ac_direct = f'{path}/{anhchinh}'
            ap_direct = path + '/AnhPhu'
            list_path_file_image['AnhChinh'] = [
                (ac_direct + '/' + filename) for filename in os.listdir(ac_direct)
            ]
            list_path_file_image['AnhPhu'] = [
                (ap_direct + '/' + filename) for filename in os.listdir(ap_direct)
            ]
    return list_path_file_image


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_code_verify():
    for i in range(3):
        # get random string of length 6 without repeating letters
        result_str = ''.join(random.sample(string.ascii_lowercase, 8))
    return result_str
