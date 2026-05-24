from django.urls import path

from duplication.views import DuplicateView, DeleteDuplicateView

urlpatterns = [
    path('', DuplicateView.as_view(), name='duplicate'),
    path('delete-duplicate/<int:duplicate_awb>', DeleteDuplicateView.as_view(), name='delete-duplicate'),
]