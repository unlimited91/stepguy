from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from externalservice.views import external_service_post_200, external_service_get_200, external_service_get_400


urlpatterns = [
    url(r'^externalservice_post/200/$', csrf_exempt(external_service_post_200), name='externalservice_post_200'),
    url(r'^externalservice_get/200/$', external_service_get_200, name='externalservice_get_200'),
    url(r'^externalservice_get/400/$', external_service_get_400, name='externalservice_get_400'),
]
