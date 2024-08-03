# views.py

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import os
import mimetypes

def media_list(request):
    media_dir = settings.MEDIA_ROOT
    path = request.GET.get('path', '').strip('/')
    
    # Prevent directory traversal attacks
    if '..' in path or path.startswith('/'):
        path = ''

    # Full path to the directory or file
    full_path = os.path.join(media_dir, path)

    if os.path.isfile(full_path):
        # If the path is a file, set the parent directory as the full_path
        full_path = os.path.dirname(full_path)

    if not os.path.exists(full_path):
        full_path = media_dir

    files_and_dirs = os.listdir(full_path)
    files_and_dirs = sorted(files_and_dirs, key=lambda x: (os.path.isdir(os.path.join(full_path, x)), x))

    items = []
    for item in files_and_dirs:
        item_path = os.path.join(path, item).replace('\\', '/')
        items.append({
            'name': item,
            'path': item_path,
            'is_dir': os.path.isdir(os.path.join(full_path, item))
        })

    selected_file = request.GET.get('file')
    if selected_file:
        selected_file_path = os.path.join(media_dir, selected_file)
        mime_type, _ = mimetypes.guess_type(selected_file_path)

        # Check if the file is a video or audio
        if mime_type and mime_type.startswith(('video/', 'audio/')):
            selected_file_url = f"{settings.MEDIA_URL}{selected_file}"
        else:
            selected_file_url = None
    else:
        selected_file_url = None

    return render(request, 'main/media_list.html', {
        'items': items,
        'selected_file': selected_file_url,
        'selected_file_name': selected_file.split('/')[-1] if selected_file else None
    })
def home(request):
    return render(request, 'main/media_list.html')