from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import NON_FIELD_ERRORS
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import ModelFormMixin

from HashTag.models import HashTag
from HashTag.models import HasgTagMembership
from InstaInfo.models import InstaInfo


class HashTagForm(forms.ModelForm):
    class Meta:
        model = HashTag
        fields = ('tag_name',)

    def clean(self):
        self.validate_unique()
        return self.cleaned_data


class HashTagCreateView(LoginRequiredMixin, CreateView):
    model = HashTag
    form_class = HashTagForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        tag_name = form.cleaned_data['tag_name']
        hash_tag = HashTag.objects.filter(tag_name=tag_name)
        if not hash_tag.exists():
            self.object.tag_name = form.cleaned_data['tag_name']
            self.object.save()

        insta_info = InstaInfo.objects.get(pk=self.kwargs['pk'])
        hash_tag_membership = HasgTagMembership(insta_info=insta_info, hash_tag=hash_tag[0])
        hash_tag_membership.save()
        return super(ModelFormMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('instainfo:detail', kwargs={'pk': self.kwargs['pk']}, )