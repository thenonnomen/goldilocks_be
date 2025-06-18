# urls.py
from django.urls import path
from .views import TestEmailView

urlpatterns = [
    path('send-email/', TestEmailView.as_view()),
]
