from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from bookms import settings
class AuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):

        white_list = settings.WHITE_LIST
        if request.path in white_list:
            return None
        if request.session.get("is_login") == True:
            return None
        else:
            return redirect('/login/')

