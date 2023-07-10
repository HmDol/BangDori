from django.views.generic import DetailView

from bangdori.models import CustomerUser


class DetailView(DetailView):
    model = CustomerUser
    context_object_name = 'target_user'
    template_name = 'myinfo.html'
