from django.urls import path
from homepage.views import HomeView, ClearDeleteView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('/delete', ClearDeleteView.as_view(), name='delete')
]