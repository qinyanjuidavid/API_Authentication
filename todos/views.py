from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from todos.serializers import TodoSerializer
from todos.models import Todo
# from django_filters.rest_framework import DjangoFilterBackend


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def CreateTodoAPIView(request):
    todoQs = Todo.objects.all()  # filter(owner=request.user)
    if request.method == "GET":
        serializer = TodoSerializer(todoQs, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
            return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
def TodoDetailAPIView(request, id):
    todoObj = Todo.objects.get(id=id,
                               # owner=request.user
                               )
    if request.method == "GET":
        serializer = TodoSerializer(todoObj, many=False)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TodoSerializer(instance=todoObj,
                                    data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == "DELETE":
        todoObj.delete()
        return Response({'todo': 'Successfully Deleted'})
