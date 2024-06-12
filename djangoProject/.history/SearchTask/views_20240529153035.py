from django.shortcuts import render

# Create your views here.
def task_detail(request):
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