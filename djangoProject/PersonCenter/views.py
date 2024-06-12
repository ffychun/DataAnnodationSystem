from django.shortcuts import render
from django.http import JsonResponse
from DataAnnodationSystem.models import User
import bcrypt
import os
from djangoProject import settings

def get_username(request):
    if request.method == 'GET':
        user_id = request.GET.get('userId')
        if user_id:
            try:
                user = User.objects.get(userID=user_id)
                username = user.name
                return JsonResponse({'username': username})
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:
            return JsonResponse({'error': 'User ID not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_headSculpturePath(request):
    if request.method == 'GET':
        user_id = request.GET.get('userId')
        if user_id:
            try:
                user = User.objects.get(userID=user_id)
                headSculpturePath = user.headSculpturePath
                return JsonResponse({'headSculpturePath': headSculpturePath})
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:
            return JsonResponse({'error': 'User ID not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def uploadAvatar(request):
    if request.method == 'POST':
        user_id = request.POST.get('userId')
        file = request.FILES.get('avatar')

        if not user_id or not file:
            return JsonResponse({'success': False, 'error': 'Missing user ID or file'})

        user = User.objects.get(userID=user_id)

        if not user:
            return JsonResponse({'success': False, 'error': 'User not found'})

        path = user.headSculpturePath
        if path and path != 'static/images/ico_uer.gif':
            path = os.path.normpath(path)
            oldPath = os.path.join(settings.MEDIA_ROOT, path)
            os.remove(oldPath)

        upload_dir = os.path.join(settings.MEDIA_ROOT, 'headSculpture')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        file_path = os.path.join(upload_dir, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        relative_path = f'headSculpture/{file.name}'
        user.headSculpturePath = relative_path
        user.save()

        return JsonResponse({'success': True, 'path': relative_path})
def personCenter(request):
    return render(request, 'personCenter.html')

def personDetail(request):
    if request.method == 'GET':
        user_id = request.GET.get('userId')
        if user_id:
            try:
                user = User.objects.get(userID=user_id)
                if user.gender == 1:
                    gender = "male"
                elif user.gender == 2:
                    gender = "female"
                else:
                    gender = ""
                user_data = {
                    'userID': user.userID,
                    'name': user.name,
                    'phone': user.phone,
                    'email': user.email,
                    'gender': gender,
                    'level': user.level
                }

                return JsonResponse({'user': user_data})
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:
            return JsonResponse({'error': 'User ID not provided'}, status=400)

    if request.method == 'POST':
        user_id = request.GET.get('userId')
        if user_id:
            try:
                user = User.objects.get(userID=user_id)
                # 更新用户信息
                user.name = request.POST.get('nickname')
                user.phone = request.POST.get('phone')
                user.email = request.POST.get('email')
                if request.POST.get('gender') == 'male':
                    user.gender = 1
                elif request.POST.get('gender') == 'female':
                    user.gender = 2
                user.save()  # 保存更新后的用户信息
                return JsonResponse({'success': True, 'message': 'User info updated successfully'})
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:
            return JsonResponse({'error': 'User ID not provided'}, status=400)

def changePassword(request):
    if request.method == 'POST':
        try:
            user_id = request.GET.get('userId')
            old_password = request.POST.get('oldPassword')
            new_password = request.POST.get('newPassword')

            # 查询用户
            try:
                user = User.objects.get(userID=user_id)
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': '用户不存在'})

            if not bcrypt.checkpw(old_password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'success': False, 'message': '旧密码错误'})

            # 修改密码
            hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.password = hashed_new_password
            user.save()

            return JsonResponse({'success': True, 'message': '密码修改成功'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': '只支持POST请求'})

def deleteUser(request):
    if request.method == 'POST':
        user_id = request.GET.get('userId')
        try:
            user = User.objects.get(userID=user_id)
            user.delete()
            return JsonResponse({'success': True, 'message': '用户注销成功'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'})
    else:
        return JsonResponse({'success': False, 'message': '请求方法错误'})

