from projectnew.settings import EMAIL_HOST, SECRET_KEY, REFRESH_TOKEN_SECRET
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import CustomerUser
import datetime
import jwt
import os
def snake_case(username, email, password):
        to = email
        html_content =  render_to_string("mail.html", {'username': username, 'password':password})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives("subject", text_content, EMAIL_HOST,[to])
        email.attach_alternative(html_content,"text/html")
        email.send()

def generate_access_token(user: CustomerUser):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              SECRET_KEY, algorithm="HS256")
    return access_token

def generate_refresh_token(user: CustomerUser) -> str:
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, REFRESH_TOKEN_SECRET, algorithm="HS256")

    return refresh_token

def get_list_path_images(path):
    import ipdb
    ipdb.set_trace()
    find_folder = os.listdir(path)
    list_path_file_image = dict()
    for folder in find_folder:
        if folder=='AnhChinh':
            ac_direct =path+'/AnhChinh'
            list_files_ac = os.listdir(ac_direct)
            link_local = []
            if list_files_ac:
                for i in list_files_ac:
                    ac = ac_direct+'/'+i
                    link_local.append(ac)
                    list_path_file_image[folder] = link_local
        if folder=='AnhPhu':
            ac_direct =path+'/AnhPhu'
            list_files_ac = os.listdir(ac_direct)
            link_local = []
            if list_files_ac:
                for i in list_files_ac:
                    ap = ac_direct+'/'+i
                    print(ap)
                    link_local.append(ap) 
                    list_path_file_image[folder] = link_local
    return list_path_file_image
