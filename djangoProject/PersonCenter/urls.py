from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('getUserName/', views.get_username),
    path('personCenter/', views.personCenter),
    path('personDetail/', views.personDetail),
    path('changePassword/', views.changePassword),
    path('deleteUser/', views.deleteUser),
    path('getHeadSculpturePath/', views.get_headSculpturePath),
    path('uploadAvatar/', views.uploadAvatar),
]