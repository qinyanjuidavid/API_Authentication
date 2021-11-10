from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from todos.serializers import TodoSerializer
from todos.models import Todo
from django_filters.rest_framework import DjangoFilterBackend
from todos.filters import TodoFilter
from rest_framework import pagination
from django.db.models import Q
from todos.pagination import StandardResultsSetPagination


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def CreateTodoAPIView(request):
    todoQs = Todo.objects.all()  # filter(owner=request.user)
    if request.method == "GET":
        # ---> First Filter
        # filterset = TodoFilter(
        #     request.GET, queryset=todoQs)
        # if filterset.is_valid():
        #     todoQs = filterset.qs
        if len(todoQs) > 0:
            query = request.GET.get('q')
            if query:
                todoQs = todoQs.filter(
                    Q(title__icontains=query) |
                    Q(id__icontains=query) |
                    Q(description__icontains=query) |
                    Q(is_complete__icontains=query)
                )
            paginator = StandardResultsSetPagination()
            result_page = paginator.paginate_queryset(todoQs, request)

            serializer = TodoSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
    elif request.method == "POST":
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                # owner=request.user
            )
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
