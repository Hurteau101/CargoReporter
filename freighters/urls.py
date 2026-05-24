from django.urls import path
from freighters.views import FreightersView

urlpatterns = [
    path('', FreightersView.as_view(), name='freighters')
]