# urls.py
from django.urls import path
from .views import SendEmailView

urlpatterns = [
    path('send-email/', SendEmailView.as_view()),
]
