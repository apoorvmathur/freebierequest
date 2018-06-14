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

    def post(self, request, format=None):
        print(request.data)
        userData = request.data
        userId = userData["user"]
        token = userData["token"]
        auth = methods.verify(userId, token)
        print(auth)
        api_result = {"status":"success"}
        if(auth):
            requestsJson = methods.getRequests(userId)
            api_result["data"]=requestsJson
        return Response(api_result)

class Approval(APIView):
    def post(self, request, format=None):
        userData = request.data
        userId = userData["user"]
        token = userData["token"]
        id = userData["id"]
        status = userData["status"]
        auth = methods.verify(userId, token)
        print(auth)
        if(auth):
            print(id)
            methods.updateRequest(id, status)
        api_result = {"status":"success"}
        return Response(api_result)

class Insert(APIView):
    def post(self, request, format=None):
        userData = request.data
        userId = userData["user"]
        token = userData["token"]
        id = userData["id"]
        status = userData["status"]
        auth = methods.verify(userId, token)
        print(auth)
        if(auth):
            print(id)
            methods.updateRequest(id, status)
        api_result = {"status":"success"}
        return Response(api_result)
