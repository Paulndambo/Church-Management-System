# middleware.py
from django.utils import timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated and hasattr(user, 'profile'):
            timezone.activate(user.profile.timezone)
        else:
            timezone.deactivate()  # fallback to default UTC

        response = self.get_response(request)
        return response
