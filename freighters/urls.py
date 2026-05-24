from django.urls import path
from freighters.views import FreightersView, AddFreighterView, EditFreighterView, DeleteFreighterView

urlpatterns = [
    path('', FreightersView.as_view(), name='freighters'),
    path('add-freighter/', AddFreighterView.as_view(), name='add-freighter'),
    path('edit-freighter/<int:freighter_id>', EditFreighterView.as_view(), name='edit-freighter'),
    path('delete-freighter/<int:freighter_id>', DeleteFreighterView.as_view(), name='delete-freighter'),
]