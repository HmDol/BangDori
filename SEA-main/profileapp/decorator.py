from django.http import HttpResponseForbidden

from .models import Profile


def profile_ownership_required(func):
    def decorated(request, *args, **kwargs):
        profile = Profile.objects.get(pk=kwargs['pk'])

        if not profile == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated