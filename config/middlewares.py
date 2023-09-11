import zoneinfo
# from backports import zoneinfo

from django.http import HttpResponseRedirect
from django.utils import translation, timezone
from django.utils.deprecation import MiddlewareMixin


class CustomLocaleMiddleware(MiddlewareMixin):
    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        if request.user.is_authenticated:
            language = request.user.system_language
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        return response


class CustomTimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            timezone.activate(zoneinfo.ZoneInfo(str(request.user.timezone)))
        return self.get_response(request)
