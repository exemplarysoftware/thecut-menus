from django.http import HttpResponse


class HttpResponseCreated(HttpResponse):
    status_code = 201

