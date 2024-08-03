from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import render
from django.conf import settings
import os

MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media')

def list_media(request):
    try:
        files = os.listdir(MEDIA_ROOT)
        files = [f for f in files if os.path.isfile(os.path.join(MEDIA_ROOT, f))]
    except FileNotFoundError:
        files = []

    return render(request, 'list_media.html', {'files': files})

def stream_media(request, filename):
    file_path = os.path.join(MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        try:
            return FileResponse(open(file_path, 'rb'))
        except Exception as e:
            # Log the exception and raise Http404
            print(f"Error streaming file {file_path}: {e}")
            raise Http404
    else:
        raise Http404
