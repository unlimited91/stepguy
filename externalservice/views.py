from django.shortcuts import render
from utils.helpers import JsonNotFoundResponse, JsonOKResponse, JsonBadRequestResponse

# Create your views here.


def external_service_get_200(request):
    return JsonOKResponse(data={
        'nova_vm_id': 'yoyo',
        'local_host_id': 'localbawa',
        'target_nova_flavor_id': 'spiderman'
    })


def external_service_get_400(request):
    return JsonBadRequestResponse(data={})


def external_service_post_200(request):
    print(f"*****************{request.body}**********************")
    return JsonOKResponse(data={
        'target_nova_vm_id': 'lllllllll'
    })
