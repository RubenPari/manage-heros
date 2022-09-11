import json
import os

import urllib3
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from heroes.models import Characters
from utils.authorization import get_params
from utils.name_string import clear_string


# get all heroes available in Marvel DB
# TODO: managing offset
def get_all_available(request):
    if request.method != 'GET':
        return HttpResponse(status=405, content='', content_type='application/json')

    endpoint = os.getenv('BASE_URL') + 'characters' + get_params()

    http = urllib3.PoolManager()
    response = http.request('GET', endpoint)

    if response.status != 200:
        return HttpResponse(status=response.status, content=response.data, content_type='application/json')

    # convert string to json
    data = json.loads(response.data)

    data = data["data"]["results"]

    heroes_list = []

    for hero in data:
        heroes_list.append({
            "id": hero["id"],
            "name": hero["name"],
            "description": hero["description"],
            "thumbnail": hero["thumbnail"]["path"] + "." + hero["thumbnail"]["extension"],
            "url": hero["resourceURI"]
        })

    heroes_list = json.dumps(heroes_list)

    return HttpResponse(heroes_list, content_type='application/json')


# get all heroes
def get_all(request):
    if request.method != 'GET':
        return HttpResponse(status=405, content='', content_type='application/json')

    heroes = Characters.objects.values_list()

    heroes_list = []

    for hero in heroes:
        heroes_list.append({
            "id": hero[0],
            "name": hero[1],
            "description": hero[2],
            "url": hero[3],
            "thumbnail": hero[4]
        })

    heroes_list = json.dumps(heroes_list)

    return HttpResponse(heroes_list, content_type='application/json')

# add new hero
@csrf_exempt
def add(request):
    if request.method != 'POST':
        return HttpResponse(status=405, content="", content_type='application/json')

    name = request.GET.get('name')

    # call endpoint to get all heroes name with all ID
    endpoint_get_heroes = "http://localhost:8000/heroes/get_all_available"

    http = urllib3.PoolManager()
    response = http.request('GET', endpoint_get_heroes)

    all_heroes = json.loads(response.data)

    hero_added = None

    # TODO: implementing offset
    # check if hero name exist in Marvel DB
    for hero in all_heroes:
        if clear_string(hero["name"]) == clear_string(name):
            hero_added = hero
            break

    if hero_added is None:
        return HttpResponse(status=404, content=json.dumps({
            "status": "error",
            "message": "hero does not exist in Marvel DB"
        }), content_type='application/json')

    # check if hero already exists in DB
    already_exists = Characters.objects.filter(name=hero_added["name"]).exists()

    if already_exists:
        return HttpResponse(status=409, content=json.dumps({
            "status": "error",
            "message": "hero already exists"
        }), content_type='application/json')

    # add hero to DB
    hero = Characters(id=hero_added["id"], name=hero_added["name"], description=hero_added["description"],
                      url=hero_added["url"],
                      thumbnail=hero_added["thumbnail"])
    hero.save()

    return HttpResponse(status=201, content=json.dumps({
        "status": "success",
        "message": "Hero added successfully"
    }), content_type='application/json')


# delete hero
@csrf_exempt
def delete(request):
    if request.method != 'DELETE':
        return HttpResponse(status=405, content="", content_type='application/json')

    id = request.GET.get('id')

    # check if hero exists
    all_heroes = Characters.objects.values_list()

    exist = False

    for hero in all_heroes:
        if hero[0] == id:
            exist = True
            break

    if not exist:
        return HttpResponse(status=404, content=json.dumps({
            "status": "error",
            "message": "hero does not exist"
        }), content_type='application/json')

    hero_deleted = Characters.objects.get(id=id)

    hero_deleted.delete()

    return HttpResponse(status=200, content=json.dumps({
        "status": "success",
        "message": "hero deleted successfully"
    }), content_type='application/json')
