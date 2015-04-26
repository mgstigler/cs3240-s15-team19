from django.conf import settings
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect

class LoginRequiredMiddleware(object):

    def process_request(self, request):
        if request.path not in settings.LOGIN_EXEMPT_URLS and not request.path.startswith('/confirm') \
                and request.user.is_anonymous():
            if request.POST:
                return login(request)
            else:
                return HttpResponseRedirect('/login/')