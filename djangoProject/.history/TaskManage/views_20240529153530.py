from django.shortcuts import render
from django.http import JsonResponse
from DataAnnodationSystem.models import Task, User
from django.utils import timezone
import os
import shutil
import zipfile

#发布者
def handle_uploaded_file(user_email, task_id, uploaded_file):
    # 检查用户文件夹是否存在，不存在则创建
    user_folder = os.path.join('media/tasks', user_email)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # 检查任务文件夹是否存在，不存在则创建
    task_folder = os.path.join(user_folder, str(task_id))
    if not os.path.exists(task_folder):
        os.makedirs(task_folder)

    # 解压上传的文件到任务文件夹
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall(task_folder)

    # 重命名任务文件夹下的文件
    file_list = os.listdir(task_folder)
    for index, file_name in enumerate(file_list, start=1):
        file_path = os.path.join(task_folder, file_name)
        new_file_name = f"{index}{os.path.splitext(file_name)[1]}"  # 构建新文件名
        new_file_path = os.path.join(task_folder, new_file_name)
        os.rename(file_path, new_file_path)

    # 返回解压后的任务文件夹路径
    return task_folder

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
        uploaded_file = request.FILES.get('dataFile')  # 获取上传的文件


        # 处理上传的数据文件
        if uploaded_file:
            user_email = user.email
            task_id = Task.objects.latest('taskId').taskId + 1  # 获取新任务的ID
            file_path = handle_uploaded_file(user_email, task_id, uploaded_file)
        else:
            file_path = ''

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
            filePath=file_path
        )
        return JsonResponse({'status': 'success', 'redirect_url': '/homePublisher/'})

    return JsonResponse({'status': 'error'})

def get_tasks_list(request):
    user_id = request.session.get('user_id')
    tasks = Task.objects.filter(userID_id=user_id).values('taskId', 'taskTitle', 'perTaskPaid', 'taskNumber', 'createTime')
    for task in tasks:
        task['createTime'] = task['createTime'].strftime('%Y-%m-%d %H:%M:%S')
    return JsonResponse({'status': 'success', 'tasks': list(tasks)})

def get_task_details(request):
    task_id = request.GET.get('task_id')
    try:
        task = Task.objects.filter(taskId=task_id).values().first()
        task['createTime'] = task['createTime'].strftime('%Y-%m-%d %H:%M:%S')
        print(task)
        return JsonResponse({'status': 'success', 'task': task})
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'})
    
#标注者
def search_tasks(request):
    return render(request,'标注者-项目搜索.html')

def get_task_information(request):
    return render(request,'标注者-我的任务.html')

def myproject2(request):
    return render(request,'标注者_我的项目.html')

