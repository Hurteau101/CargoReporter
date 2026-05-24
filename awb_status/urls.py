from django.urls import path
from awb_status.views import AWBStatusView

urlpatterns = [
    path('', AWBStatusView.as_view(), name='awb-status')
]