from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_ticket_view, name='create'),
    path('tickets/', views.list_tickets_view, name='list'),
    path('update/<str:sys_id>/', views.update_ticket_view, name='update'),
    path("assign/user/<str:sys_id>/", views.assign_user_view, name="assign_user"),
    path("assign/group/<str:sys_id>/", views.assign_group_view, name="assign_group"),
    path('delete/<str:sys_id>/', views.delete_ticket_view, name='delete'),
]
