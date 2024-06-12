from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('publish_task/', views.publish_task, name='publish_task'),
    path('get_tasks_list/', views.get_tasks_list, name='get_tasks_list'),
    path('get_task_details/', views.get_task_details, name='get_task_details'),
    path('annotator/tasksearchcenter/',views.)
]
