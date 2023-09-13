from django.shortcuts import redirect, resolve_url
from django.http import HttpResponse
from rest_framework_simplejwt.state import token_backend
from website.utils import getTokenUser

def login_required(redirect_url = "/login", raise_exception=False):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            access_token = request.COOKIES.get("access_token", None)

            try:
                decoded_payload = token_backend.decode(access_token, verify=True)
            except:
                next_url = request.get_full_path()
                path = resolve_url(redirect_url)

                if raise_exception:
                    return HttpResponse("Unauthorized", status=401)
                else:
                    return redirect(f'{path}?next={next_url}')
                
            return function(request, *args, **kwargs)
        
        return wrapper

    return decorator