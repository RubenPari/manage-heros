import json
import os

import urllib3
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from heros.models import Characters
from utils.authorization import get_params


# get all heroes
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
            "name": hero["name"],
            "description": hero["description"],
            "thumbnail": hero["thumbnail"]["path"] + "." + hero["thumbnail"]["extension"],
            "url": hero["resourceURI"]
        })

    new_data = json.dumps(new_data)

    return HttpResponse(new_data, content_type='application/json')


# add new hero
@csrf_exempt
def add(request):
    if request.method != 'POST':
        return HttpResponse(status=405, content=None, content_type='application/json')

    name = request.GET.get('name')

    # call endpoint to get all heroes name with all ID
    endpoint_get_heroes = "http://localhost:8000/heros/get_all"

    http = urllib3.PoolManager()
    response = http.request('GET', endpoint_get_heroes)

    all_heroes = json.loads(response.data)

    hero_added = None

    # TODO: implementing offset
    # check if hero name exist
    for hero in all_heroes:
        if hero["name"] == name:
            hero_added = hero
            break

    if hero_added is None:
        return HttpResponse(status=404, content="THe hero searched doesn\'t exist", content_type='application/json')

    # add hero to DB
    hero = Characters(name=hero_added["name"], description=hero_added["description"], url=hero_added["url"],
                      thumbnail=hero_added["thumbnail"])
    hero.save()

    response = json.dumps({
        "status": "success",
        "message": "Hero added successfully"
    })

    return HttpResponse(status=201, content=response, content_type='application/json')


# delete hero
@csrf_exempt
def delete(request):
    if request.method != 'DELETE':
        return HttpResponse(status=405, content=None, content_type='application/json')

    name = request.GET.get('name')

    # call endpoint to get all heroes name with all ID
    endpoint_get_heroes = "http://localhost:8000/heros/get_all"

    http = urllib3.PoolManager()
    response = http.request('GET', endpoint_get_heroes)

    all_heroes = json.loads(response.data)

    hero_deleted = None

    for hero in all_heroes:
        if hero["name"] == name:
            hero_deleted = hero
            break

    error_response = json.dumps({
        "status": "error",
        "message": "Hero searched doesn\'t exist"
    })

    if hero_deleted is None:
        return HttpResponse(status=404, content=error_response, content_type='application/json')

    # delete hero from DB
    Characters.objects.filter(name=hero_deleted["name"]).delete()

    response = json.dumps({
        "status": "success",
        "message": "Hero deleted successfully"
    })

    return HttpResponse(status=200, content=response, content_type='application/json')
