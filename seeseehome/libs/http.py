import json
from django.http import HttpResponse


def HttpJsonResponse(response_data):
    return HttpResponse(json.dumps(response_data), content_type="application/json")
