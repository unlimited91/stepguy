
from django.utils.deprecation import MiddlewareMixin
from userman.models import ApiKey
from utils.helpers import JsonNotAuthorizedResponse


class ApiAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if "admin" in request.path:
            pass
        elif "externalservice" in request.path:
            pass
        else:
            api_key = request.META['HTTP_X_APIKEY']
            try:
                request.user = ApiKey.objects.get(api_key=api_key).user
            except ApiKey.DoesNotExist:
                return JsonNotAuthorizedResponse(data={'msg': 'Incorrect creds buddy!!!!'})

