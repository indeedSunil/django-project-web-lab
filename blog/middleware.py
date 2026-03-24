# blog/middleware.py
import logging
import time
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.conf import settings

logger = logging.getLogger(__name__)

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        user = request.user if hasattr(request, 'user') else 'AnonymousUser'

        logger.info(
            f"[REQUEST]  {request.method} {request.path} | "
            f"User: {user} | IP: {request.META.get('REMOTE_ADDR')}"
        )

        response = self.get_response(request)
        duration = (time.time() - start_time) * 1000

        logger.info(
            f"[RESPONSE] {request.method} {request.path} | "
            f"Status: {response.status_code} | Time: {duration:.2f}ms"
        )
        return response

class LoginRequiredMiddleware:
    PUBLIC_URLS = ['/login/', '/register/', '/admin/', '/api/']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_public = any(
            request.path.startswith(url) for url in self.PUBLIC_URLS
        )

        if not is_public and not request.user.is_authenticated:
            # Avoid redirect loop for the login URL
            if request.path != settings.LOGIN_URL:
                return redirect(f"{settings.LOGIN_URL}?next={request.path}")
            else:
                return redirect(settings.LOGIN_URL)

        return self.get_response(request)

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' cdn.jsdelivr.net"
        return response

class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger.error(
            f"[ERROR] Unhandled exception on {request.path} | "
            f"User: {request.user} | Error: {str(exception)}",
            exc_info=True
        )
        return None
