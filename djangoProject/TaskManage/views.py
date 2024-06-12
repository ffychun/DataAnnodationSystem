from django.shortcuts import render
from django.http import JsonResponse
from DataAnnodationSystem.models import Task, User
from django.utils import timezone
import os
from djangoProject import settings
import shutil
from django.core.paginator import Paginator
from DataAnnodationSystem.models import Task

#渲染任务发布页面
def publishTask(request):
    return render(request, "publishTask.html")

#任务发布处理函数
def publish_task(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user = User.objects.get(userID=user_id)
        task_title = request.POST.get('taskTitle')
        task_description = request.POST.get('taskDescription')
        task_number = int(request.POST.get('taskNumber'))
        task_rank = int(request.POST.get('taskRank'))
        task_type = int(request.POST.get('taskType'))
        per_task_paid = float(request.POST.get('perTaskPaid'))

        Task.objects.create(
            taskTitle=task_title,
            taskDescription=task_description,
            taskNumber=task_number,
            taskRemainingNumber=task_number,
            taskRank=task_rank,
            taskType=task_type,
            perTaskPaid=per_task_paid,
            createTime=timezone.now(),
            userID=user,
            task_status='已发布'
        )
        return JsonResponse({'status': 'success', 'redirect_url': '/homePublisher/'})
    else:
        return JsonResponse({'status': 'error'})

def myPublishedTasks(request):
    return render(request, 'myPublishedTasks.html')

def get_tasks_list(request):
    user_id = request.session.get('user_id')
    tasks = Task.objects.filter(userID_id=user_id).values('taskId', 'taskTitle', 'perTaskPaid', 'taskNumber', 'createTime','task_status')
    for task in tasks:
        task['createTime'] = task['createTime'].strftime('%Y-%m-%d %H:%M:%S')
    return JsonResponse({'status': 'success', 'tasks': list(tasks)})

def get_task_details(request):
    task_id = request.GET.get('taskId')
    try:
        task = Task.objects.filter(taskId=task_id).values().first()
        task['createTime'] = task['createTime'].strftime('%Y-%m-%d %H:%M:%S')
        if task['taskType'] == 0:
            task['taskType'] = '文本'
        elif task['taskType'] == 1:
            task['taskType'] = '图像'
        else:
            task['taskType'] = '音频'
        return JsonResponse({'status': 'success', 'task': task})
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'})

def modifyTask(request):
    if request.method =='GET':
        return render(request, 'modifyTask.html')
    if request.method == 'POST':
        # 处理表单提交数据
        task_id = request.POST.get('taskId')
        task = Task.objects.get(taskId=task_id)
        try:
            if task.task_status !='已发布':
                return JsonResponse({'status': 'error', 'message': f'任务状态为{task.task_status}，已无法更改！'})
            else:
                # 根据任务 ID 更新数据库中对应的任务信息
                task.taskTitle = request.POST.get('taskTitle')
                task.taskDescription = request.POST.get('taskDescription')
                task.taskNumber = request.POST.get('taskNumber')
                task.taskRank = request.POST.get('taskRank')
                task.taskType = request.POST.get('taskType')
                task.perTaskPaid = request.POST.get('perTaskPaid')
                task.modifyTime = timezone.now()

                task.save()
                return JsonResponse({'status': 'success', 'message': '任务已删除'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

def delete_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('taskId')
        task = Task.objects.get(taskId=task_id)

        try:
            if task.task_status !='已发布':
                return JsonResponse({'status': 'error', 'message': f'任务状态为{task.task_status}，已无法删除！'})
            else:
                task.delete()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task does not exist'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# 标注者
def search_tasks(request):
    return render(request, '标注者-任务搜索.html')


def search_results(request):
    # 已完成
    task_type = request.POST.get('taskType')
    task_rank = request.POST.get('taskRank')
    task_id = request.POST.get('taskID')
    task_title = request.POST.get('taskTitle')
    min_per_task_paid = request.POST.get('minPerTaskPaid')
    max_per_task_paid = request.POST.get('maxPerTaskPaid')
    # print("task_type:",task_type)
    # print("task_rank:",task_rank)
    tasks = Task.objects.all()
    if task_type:
        tasks = tasks.filter(taskType=task_type)
    if task_rank:
        tasks = tasks.filter(taskRank=task_rank)
    if task_id:
        tasks = tasks.filter(taskId=task_id)
    if task_title:
        tasks = tasks.filter(taskTitle__icontains=task_title)
    # if min_per_task_paid and max_per_task_paid:
    #     tasks = tasks.filter(perTaskPaid__range=(min_per_task_paid, max_per_task_paid))
    if min_per_task_paid:
        tasks = tasks.filter(perTaskPaid__gte=min_per_task_paid)
    if max_per_task_paid:
        tasks = tasks.filter(perTaskPaid__lte=max_per_task_paid)

    return render(request, '标注者-搜索结果.html', {'tasks': tasks})


def task_detail(request, task_id):
    # 已完成
    task = Task.objects.get(taskId=task_id)
    task_progress = (task.taskNumber - task.taskRemainingNumber) / task.taskNumber * 100
    return render(request, '标注者-任务详情.html', {'task': task, 'task_progress': task_progress})


def task_list(request):
    # 已完成
    tasks = Task.objects.all()
    paginator = Paginator(tasks, 10)  # 每页显示10条任务
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, '标注者-任务列表.html', {'tasks': page_obj})


def homepage_annotator(request):
    # 已完成
    return render(request, '标注者-平台主页.html')
