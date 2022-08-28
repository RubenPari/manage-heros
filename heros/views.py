import os

from django.http import HttpResponse

from utils.authorization import get_params


# get all heroes with name and ID
def get_all(request):
    endpoint = os.getenv('BASE_URL') + 'characters' + get_params()
    return HttpResponse(endpoint)
