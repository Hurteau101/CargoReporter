from django.urls import path
from awb_scanner.views import GetAWBScannerView, SaveAWBScannerView, UpdateCountView, RemoveAWBScannerView, \
    MassDeleteScannerView

urlpatterns = [
    path('awb-scanner', GetAWBScannerView.as_view(), name='awb-scanner'),
    path('save-awb-scanner', SaveAWBScannerView.as_view(), name='save-awb-scanner'),
    path('update-count/<str:awb_number>', UpdateCountView.as_view(), name='update-count'),
    path('remove-awb-scanner/<str:awb_number>', RemoveAWBScannerView.as_view(), name='remove-awb-scanner'),
    path('mass-delete-awb-scanner', MassDeleteScannerView.as_view(), name='mass-delete-awb-scanner')
]