from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from rest_framework_simplejwt.state import token_backend

def getTokenUser(token:str) -> object:
    '''
        jwt token 으로부터 Usrer 반환
    '''
    try:
        decoded_payload = token_backend.decode(token, verify=True)
        user_udi = decoded_payload["user_id"]
        user = User.objects.get(pk = user_udi)

    except:
        user = None

    return user

def validate_username(username):
    '''
    아이디 유효성 체크
    '''
    try:
        RegexValidator(regex=r'^[a-zA-z0-9]{5,20}$')(username)
    except:
        return False

    blocked_username = ("admin","administrator","webmaster","manager","root")
    if username.startswith(blocked_username):
        return False

    return True

def validate_password(password):
    '''
    비밀번호 유효성 체크
    '''
    try:
        RegexValidator(regex=r'^[a-zA-z0-9!@#$%^&*()+.,~]{8,16}$')(password)
    except:
        return False

    return True

def validate_email(email):
    '''
    이메일 유효성 체크
    '''
    try:
        RegexValidator(regex=r'^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$')(email)
    except:
        return False

    return True