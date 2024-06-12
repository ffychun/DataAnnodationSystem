from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from DataAnnodationSystem.models import User, Task, Order
from djangoProject import settings
from django.contrib import messages
import os
import bcrypt
from django.urls import reverse
from django.contrib.auth import authenticate, login

def index(request):
    return render(request, 'index.html')

def register1(request):
    if request.method == 'GET':
        return render(request, '用户注册1.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(request, '该邮箱已注册，请直接登录。')
            return HttpResponse('exists')
        request.session['email'] = email
        return HttpResponse('ok')
def register2(request):
    if request.method == 'GET':
        return render(request, '用户注册2.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        user_role = request.POST.get('user-role')
        if user_role == 'publisher':
            user_role = 0
        else:
            user_role = 1

        password = request.POST.get('pwd')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        email = request.session.get('email', None)
        resume = request.FILES.get('resume')

        if resume:
            resumeFileName = f'{email}_{username}_{resume.name}'
            resume_path = os.path.join(settings.MEDIA_ROOT, 'resumes', resumeFileName) #完整路径
            with open(resume_path, 'wb+') as destination:
                for chunk in resume.chunks():
                    destination.write(chunk)

            # 保存用户信息到数据库
            user = User(
                name=username,
                permission=user_role,
                #gender=None,#0529改动
                phone='',
                status='冻结',
                email=email,
                password=hashed_password,
                resumePath=resumeFileName
            )
        else:
            user = User(
                name=username,
                permission=user_role,
                status='正常',
                #gender=None, #0529改动
                phone='',
                email=email,
                password=hashed_password,
                resumePath=''
            )
        user.save()
        return JsonResponse({'status': 'success'})
    return render(request, '用户注册2.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('user')
        password = request.POST.get('pwd')

        try:
            user = User.objects.get(email=email)
            userID = user.userID
            userType = user.permission

            if userType == 0:
                completedNum = Task.objects.filter(userID_id=userID, task_status='已完成').count()
            else:
                completedNum = Order.objects.filter(labeler_id=userID, order_state=1).count()

            if completedNum < 10:
                user.level = 1
            elif 10 <= completedNum < 20:
                user.level = 2
            elif 20 <= completedNum < 30:
                user.level = 3
            elif 30 <= completedNum < 40:
                user.level = 4
            else:
                user.level = 5

            user.save()

        except User.DoesNotExist:
            return JsonResponse({'status': 0})  # User not found

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return JsonResponse({'status': 1})  # Incorrect password

        request.session['user_id'] = user.userID
        if user.permission == 1:
            return JsonResponse({'status': 2, 'redirect_url': '/task/homepageforannotator/', 'userId': user.userID})
        elif user.permission == 0:
            return JsonResponse({'status': 2, 'redirect_url': '/homePublisher/', 'userId': user.userID})

    return render(request, 'index.html')

def homePublisher(request):
    return render(request, 'homePublisher.html')

def homeAnnotator(request):
    return render(request, 'homeAnnotator.html')

def homeAdmin(request):
    frozen_users = User.objects.filter(status='冻结')
    context = {
        'frozen_users': frozen_users,
        'MEDIA_URL': settings.MEDIA_URL,  # 添加这一行
    }
    return render(request, 'homeAdmin.html', context)

def approve_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        approval_result = request.POST.get('approval_result')
        user.approvalResult = approval_result

        if approval_result == '合格':
            user.status = '正常'
        user.save()
        messages.success(request, f'用户 {user.name} 的审批结果已保存。')
        return redirect(reverse('homeAdmin'))

    return redirect(reverse('homeAdmin'))

