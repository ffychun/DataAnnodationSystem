from django.contrib import admin
from django.urls import path
from OrderManage import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('findAllOrders/', views.findAllOrder, name='findAllOrder'),
    path('BiaozhuzheOrderList/', views.BiaozhuzheOrderList),
    path('FabuzheOrderList/', views.FabuzheOrderList),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('upload_file/<int:order_id>/<slug:file_type>/', views.upload_file, name='upload_file'),
    path('download/initial_data/<int:order_id>/', views.download_data_view, {'data_type': 'initial_data'},
         name='download_initial_data'),
    path('download/result_data/<int:order_id>/', views.download_data_view, {'data_type': 'result_data'},
         name='download_result_data'),
    path('pay/<int:order_id>/', views.pay, name='pay'),
    path('confirm_payment/<int:order_id>/', views.confirm_payment, name='confirm_payment'),
    path('createOrder/', views.createOrder, name='createOrder'),
    path('getRemainingTasks/<int:task_id>/', views.get_remaining_tasks, name='getRemainingTasks'),
]