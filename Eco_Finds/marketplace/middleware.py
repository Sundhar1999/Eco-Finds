# marketplace/middleware.py

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from django.utils import timezone
from datetime import timedelta, datetime

class AutoLogout(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        now = timezone.now()
        last_activity_str = request.session.get('last_activity', now.strftime('%Y-%m-%d %H:%M:%S'))
        last_activity = timezone.make_aware(datetime.strptime(last_activity_str, '%Y-%m-%d %H:%M:%S'))

        if (now - last_activity).seconds > 180:  # 180 seconds = 3 minutes
            logout(request)
            request.session['last_activity'] = now.strftime('%Y-%m-%d %H:%M:%S')
            return

        request.session['last_activity'] = now.strftime('%Y-%m-%d %H:%M:%S')
