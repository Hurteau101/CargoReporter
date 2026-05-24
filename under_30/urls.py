from django.urls import path

from under_30.views import Under30View, TransferAWBView, UpdateSentAWB

urlpatterns = [
    path('', Under30View.as_view(), name='under_30'),
    path('transfer-awb', TransferAWBView.as_view(), name='transfer-awb'),
    path('update-sent-awb/<str:awb_number>', UpdateSentAWB.as_view(), name='update-sent-awb'),
]