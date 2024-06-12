from django.shortcuts import render
from django.http import JsonResponse
from DataAnnodationSystem.models import Task, User
from django.utils import timezone
import os
import shutil
import zipfile
from DataAnnodationSystem.models import Task
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
    return render(request,'标注者-任务搜索.html')

def search_results(request):
    # 从请求中获取筛选条件
    task_type = request.GET.getlist('taskType')
    task_rank = request.GET.getlist('taskRank')
    task_id = request.GET.get('taskID')
    task_title = request.GET.get('taskTitle')
    min_per_task_paid = request.GET.get('minPerTaskPaid')
    max_per_task_paid = request.GET.get('maxPerTaskPaid')

    # 构建查询条件
    query = {}
    if task_type:
        query['taskType__in'] = task_type
    if task_rank:
        query['taskRank__in'] = task_rank
    if task_id:
        query['taskId'] = task_id
    if task_title:
        query['taskTitle__icontains'] = task_title
    if min_per_task_paid:
        query['perTaskPaid__gte'] = min_per_task_paid
    if max_per_task_paid:
        query['perTaskPaid__lte'] = max_per_task_paid

    # 查询任务
    tasks = Task.objects.filter(**query).values('taskId', 'taskTitle', 'perTaskPaid', 'taskNumber', 'createTime')
    for task in tasks:
        task['createTime'] = task['createTime'].strftime('%Y-%m-%d %H:%M:%S')
    # 返回搜索结果页面
    return render(request, '标注者-搜索结果.html', {'tasks': tasks})

def task_detail(request, task_id):
    try:
        task = Task.objects.get(taskId=task_id)
        return render(request, 'task_detail.html', {'task': task})
    except Task.DoesNotExist:
        return render(request, 'task_not_found.html')
    

def get_tasks_list备用(request):
    user_id = request.session.get('user_id')
    tasks = Task.objects.filter(userID_id=user_id).values('taskId', 'taskTitle', 'perTaskPaid', 'taskNumber', 'createTime')
    for task in tasks:
        task['createTime'] = task['createTime'].strftime('%Y-%m-%d %H:%M:%S')
    return JsonResponse({'status': 'success', 'tasks': list(tasks)})

def get_task_details备用(request):
    task_id = request.GET.get('task_id')
    try:
        task = Task.objects.filter(taskId=task_id).values().first()
        task['createTime'] = task['createTime'].strftime('%Y-%m-%d %H:%M:%S')
        print(task)
        return JsonResponse({'status': 'success', 'task': task})
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'})
    #return render(request,'标注者_我的任务.html')

#以下均为备用
def task_claim(request):
    return render(request,'标注者-任务申领.html')

def myproject2(request):
    return render(request,'标注者_我的任务.html')

def get_task(request):
    user=request.COOKIES['user']
    task_id=request.POST['project_id']
    with database_connection() as cursor:
        cursor.execute("insert into user_task values('%s','%s','%s')"%(user,task_id,0))
        cursor.execute("update task set statu='1' where task_id='%s'"%task_id)
    return HttpResponse('')

def begin_task(request):
    task_type=request.GET['project_type']
    task_id=request.GET['task_id']
    project_name=request.GET['project_name']
    with database_connection() as cursor:
        cursor.execute("select [index],length from task where task_id='%s'"%task_id)
        index,length=cursor.fetchall()[0]
    url=''
    index=int(index)
    length=int(length)
    for i in range(int(length)):
        url+=('/static/project/'+project_name+'/'+str(index+i)+change_type(task_type)+'\n')
    if task_type=='IMAGE':
        return render(request,'标注者_图片任务标注.html',locals())
    if task_type=='AUDIO':
        return render(request,'标注者_图片任务标注.html',locals())
    if task_type=='VIDEO':
        return render(request,'标注者_图片任务标注.html',locals())

def del_task(request):
    task_id=request.POST['task_id']
    with database_connection() as cursor:
        cursor.execute("delete from user_task where task_id='%s'"%task_id)
        cursor.execute("update task set statu=0 where task_id='%s'"%task_id)
    return HttpResponse('')

def save_result(request):
    dat=json.loads(request.POST['dat'])
    task_id=dat['project']['pname']
    with database_connection() as cursor:
        cursor.execute("update task set statu=2 where task_id='%s'"%task_id)
    path=os.path.join(settings.BASE_DIR,"static","result","%s.json"%task_id)
    with open(path, 'w') as f:
        json.dump(dat, f)
    return mission_information(request)
