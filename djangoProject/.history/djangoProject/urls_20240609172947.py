"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from RegisterLogin import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path('index', views.index),#0529新加入
    path('register1/', views.register1),
    path('register2/', views.register2),
    path('login/', views.login),
    path('homePublisher/', views.homePublisher),
    path('homeAnnotator/', views.homeAnnotator),
    path('homeAdmin/', views.homeAdmin, name='homeAdmin'),
    path('approve_user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('task/', include('TaskManage.urls')),
    path('personCenter/', include('PersonCenter.urls')),
    path('OrderManage/', include("OrderManage.urls")),
    path('AnnotationMethod/', include("AnnotationMethod.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

