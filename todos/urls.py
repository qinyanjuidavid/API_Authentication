from django.urls import path
from todos import views

app_name = 'todos'

urlpatterns = [
    path('', views.CreateTodoAPIView)
]
