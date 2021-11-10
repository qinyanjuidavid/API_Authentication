from django.urls import path
from todos import views

app_name = 'todos'

urlpatterns = [
    path('', views.CreateTodoAPIView, name="todo-create"),
    path('<int:id>/', views.TodoDetailAPIView, name='todo-detail'),
]
