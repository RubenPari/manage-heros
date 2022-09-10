import json
import os

import urllib3
from django.http import HttpResponse

from utils.authorization import get_params


# return all comics where compare
# the specific hero
def get_all_available_by_hero(request):
    if request.method != 'GET':
        return HttpResponse(status=405, content=None, content_type='application/json')

    endpoint = os.getenv('BASE_URL') + 'characters/' + request.GET.get('character_id') + '/comics' + get_params()

    http = urllib3.PoolManager()
    response = http.request('GET', endpoint)

    error_response = json.dumps({
        "status": "error",
        "message": "error getting all comics from Marvel DB"
    })

    if response.status != 200:
        return HttpResponse(status=response.status, content=error_response, content_type='application/json')

    data = json.loads(response.data)

    data = data["data"]["results"]

    data = json.dumps(data)

    # TODO: edit original objects
    """
    comics_list = []
    
    for comic in data:
        comics_list.append({
            "id": comic["id"],
            "title": comic["title"],
            "description": comic["description"],
            "thumbnail": comic["thumbnail"]["path"] + "." + comic["thumbnail"]["extension"]
        })
    
    comics_list = json.dumps(comics_list)
    """
    return HttpResponse(data, content_type='application/json')
