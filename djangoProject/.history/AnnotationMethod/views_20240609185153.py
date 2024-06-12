from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Example
from django.conf import settings
import json,csv,os
from django.shortcuts import render, redirect
from .models import TaggedLine

def index(request):
    data = {'project_detail': 'Your project details here'}  # Replace with your actual data
    return render(request, 'hello.html', {'data': data})

def info(request):
    return render(request, 'info.html')

def help(request):
    return render(request, 'help.html', {'message': '使用帮助'})


def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        file_content = uploaded_file.read().decode('utf-8')
        lines = file_content.split('\n')
        total_lines = len(lines)
        request.session['total_lines'] = total_lines
        request.session['lines'] = lines  # 设置会话变量
        # 其他处理文件的代码...
        # return JsonResponse({'status': 'success', 'total_lines': total_lines})
        return redirect('tag_lines')
    return render(request, 'upload.html')

def tag_lines(request):
    # 获取当前标注的行号
    current_line_number = request.session.get('current_line_number', 1)
    # 获取总行数
    total_lines = request.session.get('total_lines', 0)
    # 获取当前行文本
    lines = request.session.get('lines', [])
    current_line_text = lines[current_line_number - 1] if lines else ''
    # 渲染标注页面
    context = {
        'line_number': current_line_number,
        'line_text': current_line_text,
        'total_lines': total_lines
    }
    return render(request, 'tag_lines.html', context)


def save_tag(request):
    if request.method == 'POST':
        line_number = request.POST.get('line_number')
        line_text = request.POST.get('line_text')
        tag = request.POST.get('tag')
        # if not file_path:
        #     return JsonResponse({'error': 'File path is missing'}, status=400)
        
        print(f"Received data: line_number={line_number}, line_text={line_text}, tag={tag}")
        email = request.session.get('email', None)
        FileName = f'{email}_tags.csv'
        file_path = os.path.join(settings.MEDIA_ROOT, 'Tagging', FileName) #完整路径
        write_header = not os.path.exists(file_path) or os.path.getsize(file_path) == 0
        try:
            
            with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([line_number, line_text, tag])
        except Exception as e:
            print(f"Error writing to CSV file: {e}")
            return JsonResponse({'error': 'Failed to write to CSV file'}, status=500)

        # 保存标签到数据库
        try:
            TaggedLine.objects.create(line_number=line_number, tag=tag)
        except Exception as e:
            print(f"Error saving to database: {e}")
            return JsonResponse({'error': 'Failed to save to database'}, status=500)

        # 确定是否所有行都已标记
        total_lines = request.session.get('total_lines', 0)
        all_lines_tagged = int(line_number) >= total_lines
        # print(int(line_number))
        #print(all_lines_tagged)
        if all_lines_tagged:
            return JsonResponse({'status': 'completed'})
        else:
            # Load the next line
            next_line_number = int(line_number) + 1
            return redirect('get_line', line_number=next_line_number)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_line(request, line_number):

    lines = request.session.get('lines', [])
    current_line_text = lines[line_number - 1] if lines else ''

    # Calculate the total number of lines
    total_lines = request.session.get('total_lines', 0)

    # Prepare the context data
    context = {
        'line_number': line_number,
        'line_text': current_line_text,
        'total_lines': total_lines
    }
    # Render the tag_lines.html template with the context data
    return render(request, 'tag_lines.html', context)