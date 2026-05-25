from django.urls import path
from awb_status.views import AWBStatusView, UploadImageView, DeleteImageView

urlpatterns = [
    path('', AWBStatusView.as_view(), name='awb-status'),
    path('upload-image/<str:awb_number>', UploadImageView.as_view(), name='upload-image'),
    path('delete-image/<str:awb_number>', DeleteImageView.as_view(), name='delete-image'),
]