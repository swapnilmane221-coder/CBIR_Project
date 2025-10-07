from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from models.resnet_feature_extractor import get_similar_images
import os
from django.conf import settings
import shutil

def upload_image(request):
    if request.method == "POST" and request.FILES.get("query_image"):
        uploaded_file = request.FILES["query_image"]
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "queries"))
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        # Get similar images
        results = get_similar_images(file_path)

        # Copy retrieved dataset images to MEDIA folder for serving
        media_result_paths = []
        for img_path in results:
            dest_path = os.path.join(settings.MEDIA_ROOT, "results", os.path.basename(img_path))
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(img_path, dest_path)
            media_result_paths.append(settings.MEDIA_URL + "results/" + os.path.basename(img_path))

        return render(request, "cbir_app/results.html", {
            "query": settings.MEDIA_URL + "queries/" + uploaded_file.name,
            "results": media_result_paths,
        })

    return render(request, "cbir_app/upload.html")
