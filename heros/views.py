import json
import os

import urllib3
from django.http import HttpResponse

from utils.authorization import get_params


# get all heroes with name and ID
# TODO: managing offset
def get_all(request):
    endpoint = os.getenv('BASE_URL') + 'characters' + get_params()

    http = urllib3.PoolManager()
    response = http.request('GET', endpoint)

    if response.status != 200:
        return HttpResponse(status=response.status, content=response.data, content_type='application/json')

    data = response.data

    # convert string to json
    data = json.loads(data)

    data = data["data"]["results"]

    # create new list with name and ID
    new_data = []

    for hero in data:
        new_data.append({
            "id": hero["id"],
            "name": hero["name"]
        })

    new_data = json.dumps(new_data)

    return HttpResponse(new_data, content_type='application/json')
