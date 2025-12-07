from django.shortcuts import render
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from .ocr import extract_text_from_image

def index(request):
    return render(request, 'index.html')

class OCRAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES:
            return Response({"error": "No image provided"}, status=400)

        image_file = request.FILES['image']
        rel_path = default_storage.save(f"temp/{image_file.name}", image_file)
        
        try:
            file_path = default_storage.path(rel_path)
        except Exception:

            file_path = os.path.join(settings.MEDIA_ROOT, rel_path)

        try:
            text = extract_text_from_image(file_path)
            return Response({"text": text})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        finally:
            
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                pass
