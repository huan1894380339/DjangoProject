from __future__ import annotations

import datetime
import os

import jwt
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework_simplejwt.tokens import RefreshToken
from projectnew.settings import EMAIL_HOST, REFRESH_TOKEN_SECRET, SECRET_KEY
from .models import CustomerUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from json2html import json2html
import pdfkit


def send_email(user, current_site, html):
    to = user.email
    html_content = render_to_string(
        html,
        {
            'domain': current_site.domain, 'uid': urlsafe_base64_encode(
                force_bytes(user.id),
            ), 'token': default_token_generator.make_token(user),
        },
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


def active(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomerUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomerUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomerUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomerUser.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        password = CustomerUser.objects.make_random_password()
        user.set_password(password)
        user.save()
        return HttpResponse(f'Now you can login your account with password: {password}')
    else:
        return HttpResponse('Activation link is invalid!')


class PdfConverter(object):

    def __init__(self):
        pass

    def to_html(self, json_doc):
        return json2html.convert(json=json_doc)

    def to_pdf(self, html_str):
        config = pdfkit.configuration(
            wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe',
        )
        return pdfkit.from_string(html_str, None, configuration=config)
