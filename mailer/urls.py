from django.urls import path
from .views import agent_form

urlpatterns = [
    path('agent-form/', agent_form, name='agent_form'),
]
