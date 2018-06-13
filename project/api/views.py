from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from project.api.methods import methods
from project.api.tasks import tasks

class User(APIView):
    def post(self, request, format=None):
        print(request.data)
        userData = request.data
        auth = methods.authenticate(userData["user"], userData["password"])
        api_result = {"auth":auth}
        if auth:
            token = tasks.generateToken(userData["user"])
            api_result["token"] = token
        return Response(api_result)

class FreebieRequest(APIView):

    def get(self, request, format=None):

        # View Logic Here
        api_result = {"key_1":"val_1", "key_2":"val_2"}
        return Response(api_result)
