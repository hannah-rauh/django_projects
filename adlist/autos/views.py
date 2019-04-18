from autos.models import Auto, Comment

from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from autos.util import AutosListView, AutosDetailView, AutosCreateView, AutosUpdateView, AutosDeleteView
from autos.forms import CreateForm, CommentForm


class AutoListView(AutosListView):
    model = Auto
    template_name = "auto_list.html"

class AutoDetailView(AutosDetailView):
    model = Auto
    template_name = "auto_detail.html"

    def get(self, request, pk) :
        auto = Auto.objects.get(id=pk)
        comments = Comment.objects.filter(auto=auto).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'auto' : auto, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class AutoCreateView(AutosCreateView):
    model = Auto
    fields = ['name', 'detail', 'mileage']
    template_name = "auto_form.html"
    success_url = reverse_lazy('autos')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Autod autos to the model before saving
        auto = form.save(commit=False)
        auto.owner = self.request.user
        auto.save()
        return redirect(self.success_url)


class AutoUpdateView(AutosUpdateView):
    model = Auto
    fields = ['name', 'detail', 'mileage']
    template_name = "auto_form.html"
    success_url = reverse_lazy('autos')
    def get(self, request, pk) :
        auto = get_object_or_404(Auto, id=pk, owner=self.request.user)
        form = CreateForm(instance=auto)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        auto = get_object_or_404(Auto, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=auto)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

class AutoDeleteView(AutosDeleteView):
    model = Auto
    template_name = "auto_delete.html"


class AutoFormView(LoginRequiredMixin, View):
    template = 'auto_form.html'
    success_url = reverse_lazy('autos')

    def get(self, request, pk=None) :
        if not pk :
            form = CreateForm()
        else:
            auto = get_object_or_404(Auto, id=pk, owner=self.request.user)
            form = CreateForm(instance=auto)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            auto = get_object_or_404(Auto, id=pk, owner=self.request.user)
            form = CreateForm(request.POST, request.FILES or None, instance=auto)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Autojust the model autos before saving
        auto = form.save(commit=False)
        auto.owner = self.request.user
        auto.save()
        return redirect(self.success_url)

class CommentCreateView(LoginRequiredMixin, View):
    template = 'auto_form.html'
    success_url = reverse_lazy('autos')

    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk) :
        f = get_object_or_404(Auto, id=pk)
        comment_form = CommentForm(request.POST)

        comment = Comment(text=request.POST['comment'], owner=request.user, auto=f)
        comment.save()
        return redirect(reverse_lazy('auto_detail', args=[pk]))

class CommentDeleteView(AutosDeleteView):
    model = Comment
    template_name = "auto_comment_delete.html"

    def get_success_url(self) :
        auto = self.object.auto
        return reverse_lazy('auto_detail', args=[auto.id])
