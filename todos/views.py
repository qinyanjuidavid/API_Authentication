from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from todos.serializers import TodoSerializer
from todos.models import Todo


@api_view(['GET', 'POST'])
def CreateTodoAPIView(request):
    todoQs = Todo.objects.all()
    if request.method == "GET":
        serializer = TodoSerializer(todoQs, many=True)
        return Response(serializer.data)
