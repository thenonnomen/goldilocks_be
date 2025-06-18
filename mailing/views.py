from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View
from django.core.mail import send_mail


class TestEmailView(View):
    def get(self, request):
        send_mail(
            subject='Django Email Test',
            message='If you received this, email config works!',
            from_email='test@example.com',
            recipient_list=['recipient@example.com'],
        )
        return JsonResponse({'status': 'Email sent'})

"""
python -m smtpd -c DebuggingServer -n localhost:1025

To run the smtp server in terminal
"""