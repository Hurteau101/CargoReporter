import cloudinary.uploader
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from awb_status.models import AWBStatus


"""
This view is in charge of handling:
- Uploading images + uploading to Cloudinary
- Deleting images
- Displaying the AWB status
"""

class DeleteImageView(View):
    def delete(self, request, awb_number):
        awb = AWBStatus.objects.get(awb_number=awb_number)
        if awb.image:
            # Delete the image from Cloudinary and save as None
            cloudinary.uploader.destroy(awb.image.name)
            awb.image = None
            awb.save()
        return JsonResponse({'message': 'Image removed'}, status=200)

class UploadImageView(View):
    def post(self, request, awb_number):
        image = request.FILES.get('img')
        if not image:
            return JsonResponse({'message': 'No image provided'}, status=400)

        awb = AWBStatus.objects.get(awb_number=awb_number)
        awb.image = image
        awb.save()

        return JsonResponse({'image_url': awb.image.url}, status=200)

class AWBStatusView(View):
    def get(self, request):
        awb_status = AWBStatus.objects.all()

        return render(request, 'awb_status.html', context={'awb_status': awb_status})