from django.urls import path
from freighters.views import FreightersView, AddFreighterView

urlpatterns = [
    path('', FreightersView.as_view(), name='freighters'),
    path('add-freighter/', AddFreighterView.as_view(), name='add-freighter')
]