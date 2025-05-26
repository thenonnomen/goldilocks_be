# Middleware to record all user actions.
import json
from .models import UserHistory
from django.utils.deprecation import MiddlewareMixin

SENSITIVE_KEYS = ['password', 'token', 'authorization', 'auth', 'secret']

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            body = request.body.decode('utf-8') if request.body else ''
            # Try to parse JSON body if applicable
            if 'application/json' in request.content_type:
                data = json.loads(body)
                for key in data:
                    if any(s in key.lower() for s in SENSITIVE_KEYS):
                        data[key] = '[REDACTED]'
                body = json.dumps(data)
        except Exception:
            body = '[Unreadable Body]'

        # Filter headers
        headers = {}
        for k, v in request.headers.items():
            if any(s in k.lower() for s in SENSITIVE_KEYS):
                headers[k] = '[REDACTED]'
            else:
                headers[k] = v

        UserHistory.objects.create(
            method=request.method,
            path=request.path,
            headers=json.dumps(headers),
            body=body[:5000],  # Truncate to avoid overloading
            user=request.user if request.user.is_authenticated else None
        )