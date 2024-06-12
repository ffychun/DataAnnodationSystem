import datetime
from django.contrib import messages
from django.http import HttpResponse, FileResponse, JsonResponse
from DataAnnodationSystem.models import User, Order, Task
from djangoProject import settings
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.db.models import F
import os


def BiaozhuzheOrderList(request):
    return render(request, '标注者-我的订单.html')


def FabuzheOrderList(request):
    return render(request, '发布者-我的订单.html')


def findAllOrder(request):
    if 'user_id' in request.session:
        try:
            user_id = request.session.get('user_id')
            user = User.objects.get(userID=user_id)
            if user.permission == 0:
                all_orders = Order.objects.filter(publisher_id=user_id)
            elif user.permission == 1:
                all_orders = Order.objects.filter(labeler_id=user_id)
            orders_data = list(all_orders.values())
            return JsonResponse({'status': 'success', 'orders': orders_data})
        except Exception as e:
            return JsonResponse({'status': 'error'})
    else:
        return JsonResponse({'status': 'error'})


def order_detail(request, order_id):
    order = Order.objects.get(order_id=order_id)
    task = Task.objects.get(taskId=order.task_id)
    user = User.objects.get(userID=task.userID_id)
    publisher = User.objects.get(userID=order.publisher_id)
    if order.submit_time:
        submit_time = order.submit_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        submit_time = None

    orders_data = {
        'order_id': order.order_id,
        'task_id': task.taskTitle,
        'task_creator': user.name,
        'task_description': task.taskDescription,
        'order_state': order.get_order_state_display(),
        'total_price': order.total_price,
        'payment_status': '未支付' if order.pay_method == 0 else '已支付',
        'create_time': order.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'submit_time': submit_time,
        'task_creator_name': publisher.name,
    }

    return JsonResponse({'status': 'success', 'orderDetails': orders_data})

def upload_file(request, order_id, file_type):
    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '订单不存在'})

    if file_type == 'result_file' and not order.dataset_path:
        return JsonResponse({'status': 'error', 'message': '请等待发布者上传原始数据'})

    if request.method == 'POST' and file_type in request.FILES:
        uploaded_file = request.FILES[file_type]

        if file_type == 'dataset_file':
            file_path = f"initial_data/{order.order_id}_{uploaded_file.name}"
        elif file_type == 'result_file':
            file_path = f"result_data/{order.order_id}_{uploaded_file.name}"

        full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

        try:
            with open(full_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            if file_type == 'dataset_file':
                order.dataset_path = file_path
            elif file_type == 'result_file':
                order.result_path = file_path
                order.submit_time = datetime.datetime.now()

            order.save()
            return JsonResponse({'status': 'success', 'message': '上传成功'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': '上传失败，请稍后重试'})
    else:
        return JsonResponse({'status': 'error', 'message': '请先选择文件'})


def download_data_view(request, order_id, data_type):
    order = get_object_or_404(Order, order_id=order_id)

    if data_type == 'initial_data':
        file_path = order.dataset_path
    elif data_type == 'result_data':
        file_path = order.result_path

    full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    print(file_path)

    try:
        file = open(full_file_path, 'rb')
        response = FileResponse(file)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(full_file_path)}"'
        return response
    except FileNotFoundError:
        return HttpResponse("File not found.")


def pay(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        return render(request, '发布者-支付页面.html', {'order': order})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)


def confirm_payment(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        messages.error(request, '订单不存在')
        return redirect('pay', order_id=order_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        redirect_url = request.META.get('HTTP_REFERER')
        if payment_method:
            try:
                order.pay_method = int(payment_method)
                order.order_state = 1
                order.save()
                return HttpResponse(f"<script>alert('支付成功'); window.location.href = '{redirect_url}';</script>")
            except ValueError:
                return HttpResponse(f"<script>alert('无效的支付方式'); window.location.href = '{redirect_url}';</script>")
        else:
            return HttpResponse(f"<script>alert('请选择支付方式'); window.location.href = '{redirect_url}';</script>")


def confirm_pay(request):
    if request.method == 'POST':
        payment_status = 'success'
        response_data = {'status': payment_status}
        return JsonResponse(response_data)

def createOrder(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        task_id = request.POST.get('taskId')
        redirect_url = request.META.get('HTTP_REFERER')
        selected_task_number = int(request.POST.get('selected_task_number'))
        task = Task.objects.get(taskId=task_id)
        user = User.objects.get(userID=user_id)
        if selected_task_number == 0 or task.taskRemainingNumber <= 0 or selected_task_number > task.taskRemainingNumber:
            return HttpResponse(f"<script>alert('任务编号无效'); window.location.href = '{redirect_url}';</script>")
        if user.status != '正常':
            return HttpResponse(f"<script>alert('您的账号异常'); window.location.href = '{redirect_url}';</script>")
        if user.level < task.taskRank:
            return HttpResponse(f"<script>alert('您的等级不足'); window.location.href = '{redirect_url}';</script>")

        task.taskRemainingNumber = F('taskRemainingNumber') - selected_task_number
        task.save()

        per_task_price = task.perTaskPaid
        total_price = selected_task_number * per_task_price

        order_id = Order.objects.count() + 1

        new_order = Order(
            order_id=order_id,
            task_id=task.taskId,
            publisher_id=task.userID.userID,
            labeler_id=user.userID,
            order_state=0,
            total_price=total_price,
            pay_method=0,
            create_time=datetime.datetime.now()
        )
        new_order.save()
        return HttpResponse(f"<script>alert('订单创建成功'); window.location.href = '{redirect_url}';</script>")

    else:
        return HttpResponse("This URL only accepts POST requests")


def get_remaining_tasks(request, task_id):
    try:
        task = Task.objects.get(taskId=task_id)
        return JsonResponse({'remainingTasks': task.taskRemainingNumber})
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)