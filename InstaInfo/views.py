from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import *
from InstaInfo.models import InstaInfo
from HashTag.models import HasgTagMembership
from HashTag.models import HashTag


# Create your views here.

class InstaInfoListView(LoginRequiredMixin, ListView):
    model = InstaInfo
    context_object_name = 'instainfos'

    def get_queryset(self):
        return InstaInfo.objects.filter(owner=self.request.user)


class InstaInfoCreateView(LoginRequiredMixin, CreateView):
    model = InstaInfo
    fields = ['insta_account', 'insta_passwd']
    success_url = reverse_lazy('instainfo:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(InstaInfoCreateView, self).form_valid(form)


class InstaInfoDetailView(LoginRequiredMixin, DetailView):
    model = InstaInfo

    def get_context_data(self, **kwargs):
        context = super(InstaInfoDetailView, self).get_context_data(**kwargs)
        insta_info = InstaInfo.objects.get(pk=self.kwargs['pk'])
        context['hash_tag'] = HashTag.objects.filter(insta_info__insta_account=insta_info)
        return context


class InstaInfoUpdateView(LoginRequiredMixin, UpdateView):
    model = InstaInfo
    fields = ['insta_account', 'insta_passwd']
    success_url = reverse_lazy('instainfo:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(InstaInfoUpdateView, self).form_valid(form)


class InstaInfoDeleteView(LoginRequiredMixin, DeleteView):
    model = InstaInfo
    success_url = reverse_lazy('instainfo:index')
