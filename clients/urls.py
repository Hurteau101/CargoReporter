from django.urls import path

from clients.views import ClientsView, AddClientView, EditClientView, DeleteClientView

urlpatterns = [
    path('', ClientsView.as_view(), name='clients'),
    path('add-client/', AddClientView.as_view(), name='add-client'),
    path('edit-client/<int:client_id>', EditClientView.as_view(), name='edit-client'),
    path('delete-client/<int:client_id>', DeleteClientView.as_view(), name='delete-client'),
]