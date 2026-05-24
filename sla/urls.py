from django.urls import path

from sla.views import SLAView

urlpatterns = [
    path('', SLAView.as_view(), name='sla')
]