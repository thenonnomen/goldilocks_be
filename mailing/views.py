from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View
from django.core.mail import send_mail


class SendEmailView(View):
    def get(self, request):
        send_mail(
            'Brevo SMTP Test',
            'Email sent via Brevo SMTP!',
            '8f991a001@smtp-brevo.com',
            ['ananthu.nair707@gmail.com', 'akashsivaramakrishnan96@gmail.com'],  # Replace with actual target
        )
        return JsonResponse({'message': 'Email sent via Brevo SMTP'})

"""
python -m smtpd -c DebuggingServer -n localhost:1025

To run the smtp server in terminal

ananthu.nair707@gmail.com
"""