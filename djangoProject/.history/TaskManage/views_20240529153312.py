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
def my_task(request):
    user=request.COOKIES['user']
    json_list=[]
    count=0
    try:
        with database_connection() as cursor:
            cursor.execute("""select distinct task.task_id,project_name,project_type,project_description,
                           project_level,project_deadline,length,statu from project,task,user_task
                       where project.project_id=task.project_id and
                       task.task_id in(select user_task.task_id from user_task where user_task.[user]='%s')"""%user)
            information=cursor.fetchall()
        for item in information:
            count+=1
            json_list.append({'project_id':item[0],
                              'project_name':encoding(item[1]),
                              'project_type':item[2],
                              'description':encoding(item[3]),
                              'level':item[4],
                              'deadline':item[5],
                              'task_num':item[6],
                              'statu':encoding(statu(item[7])),
                              })
        return JsonResponse({"code": 0,"msg": "","count": count,"data":json_list})
    except:
        return JsonResponse({"code": 0,"msg": "","count": count,"data":json_list})
    return

def get_task_details_for_annodater(request):
    task_id=request.GET['id']
    with database_connection() as cursor:
        cursor.execute("""select task.task_id,finish,project.project_id,project_name,project_type,
                       project_description,project_level,project_deadline,project_reward,project.[user]
                       from project,task,user_task
                       where project.project_id=task.project_id and user_task.task_id=task.task_id
                       and task.task_id='%s'"""%task_id)
        item=cursor.fetchall()[0]
    task_id=item[0]
    finish=item[1]
    project_id=item[2]
    project_name=item[3]
    project_type=item[4]
    project_description=item[5]
    project_level=item[6]
    project_deadline=item[7]
    project_reward=item[8]
    project_user=item[9]
    return render(request,'标注者_任务详情.html',encoding_dic(locals()))
def get_mission(request):
    return render(request,'标注者_项目搜索.html')

def mission_information(request):
    return render(request,'标注者_我的任务.html')

def myproject2(request):
    return render(request,'标注者_我的项目.html')

