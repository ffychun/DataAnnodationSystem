from django.urls import path
from django.http import HttpResponse
from . import views
# from .views import run_command

# def ignore_favicon(request):
#     return HttpResponse('')

# urlpatterns = [
#     # ... 其他URL模式 ...
#     path('', run_command, name='run_command'),
#     # path('favicon.ico', ignore_favicon),  # 忽略favicon请求
# ]
urlpatterns = [
    path('', views.index, name='index'),
    path('help/', views.help, name='help'),
    path('info/', views.info, name='info'),
    path('upload/', views.upload_file, name='upload_file'),
    path('tag_lines/', views.tag_lines, name='tag_lines'),
    path('save_tag/', views.save_tag, name='save_tag'),
    path('tag_lines/<int:line_number>/', views.get_line, name='get_line'),
    path('download/', views.download_dataset, name='download_dataset'),
]