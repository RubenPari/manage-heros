import json
import os

import urllib3
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from comics.models import Comic
from utils.authorization import get_params
from utils.name_string import clear_string


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

    comics_list = []

    for comic in data:
        comics_list.append({
            "id": comic["id"],
            "title": comic["title"],
            "description": comic["description"],
            "isbn": comic["isbn"],
            "ean": comic["ean"],
            "format": comic["format"],
            "pageCount": comic["pageCount"],
            "resourceURI": comic["resourceURI"],
            "url": comic["urls"][0]["url"],
            "thumbnail": comic["thumbnail"]["path"] + "." + comic["thumbnail"]["extension"]
        })

    comics_list = json.dumps(comics_list)

    return HttpResponse(comics_list, content_type='application/json')


def get_all(response):
    if response.method != 'GET':
        return HttpResponse(status=405, content=None, content_type='application/json')

    comics = Comic.objects.values_list()
    comics_list = []

    for comic in comics:
        comics_list.append({
            "id": comic[0],
            "title": comic[1],
            "description": comic[2],
            "isbn": comic[3],
            "ean": comic[4],
            "format": comic[5],
            "pageCount": comic[6],
            "resourceURI": comic[7],
            "url": comic[8],
            "thumbnail": comic[9]
        })

    comics_list = json.dumps(comics_list)

    return HttpResponse(comics_list, content_type='application/json')


# add a new comic
@csrf_exempt
def add(request):
    if request.method != 'POST':
        return HttpResponse(status=405, content="", content_type='application/json')

    body_request = json.loads(request.body)

    endpoint = "http://localhost:8000/comics/get_all_available?character_id=" + str(body_request["character_id"])

    http = urllib3.PoolManager()
    response = http.request('GET', endpoint)

    error_response = json.dumps({
        "status": "error",
        "message": "error getting all comics from Marvel DB"
    })

    if response.status != 200:
        return HttpResponse(status=response.status, content=error_response, content_type='application/json')

    data = json.loads(response.data)

    # check if the comic with name exists in Marvel DB
    comic_found = None

    for comic in data:
        if clear_string(comic["title"]) == clear_string(body_request["title"]):
            comic_found = comic
            break

    error_response = json.dumps({
        "status": "error",
        "message": "comic doesn't exist in Marvel DB"
    })

    if comic_found is None:
        return HttpResponse(status=404, content=error_response, content_type='application/json')

    # check if the comic with name exists in DB
    exists = Comic.objects.filter(id=comic_found["id"]).exists()

    error_response = json.dumps({
        "status": "error",
        "message": "comic already exists in DB"
    })

    if exists:
        return HttpResponse(status=409, content=error_response, content_type='application/json')

    # add the comic in DB
    comic = Comic(
        id=comic_found["id"],
        title=comic_found["title"],
        description=comic_found["description"],
        isbn=comic_found["isbn"],
        ean=comic_found["ean"],
        format=comic_found["format"],
        pageCount=comic_found["pageCount"],
        resourceURI=comic_found["resourceURI"],
        url=comic_found["url"],
        thumbnail=comic_found["thumbnail"]
    )

    comic.save()

    success_response = json.dumps({
        "status": "ok",
        "message": "comic added successfully"
    })

    return HttpResponse(status=201, content=success_response, content_type='application/json')
