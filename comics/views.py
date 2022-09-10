from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the comics index.", status=200, content_type='text/plain')
