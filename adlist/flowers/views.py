from flowers.models import Flower, Comment

from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from flowers.util import FlowersListView, FlowersDetailView, FlowersCreateView, FlowersUpdateView, FlowersDeleteView
from flowers.forms import CreateForm, CommentForm


class FlowerListView(FlowersListView):
    model = Flower
    template_name = "flower_list.html"

class FlowerDetailView(FlowersDetailView):
    model = Flower
    template_name = "flower_detail.html"

    def get(self, request, pk) :
        flower = Flower.objects.get(id=pk)
        comments = Comment.objects.filter(flower=flower).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'flower' : flower, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class FlowerCreateView(FlowersCreateView):
    model = Flower
    fields = ['name', 'detail', 'mileage']
    template_name = "flower_form.html"
    success_url = reverse_lazy('flowers')
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
        flower = form.save(commit=False)
        flower.owner = self.request.user
        flower.save()
        return redirect(self.success_url)


class FlowerUpdateView(FlowersUpdateView):
    model = Flower
    fields = ['name', 'detail', 'mileage']
    template_name = "flower_form.html"
    success_url = reverse_lazy('flowers')
    def get(self, request, pk) :
        flower = get_object_or_404(Flower, id=pk, owner=self.request.user)
        form = CreateForm(instance=flower)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        flower = get_object_or_404(Flower, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=flower)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

class FlowerDeleteView(FlowersDeleteView):
    model = Flower
    template_name = "flower_delete.html"


class FlowerFormView(LoginRequiredMixin, View):
    template = 'flower_form.html'
    success_url = reverse_lazy('flowers')

    def get(self, request, pk=None) :
        if not pk :
            form = CreateForm()
        else:
            flower = get_object_or_404(Flower, id=pk, owner=self.request.user)
            form = CreateForm(instance=flower)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            flower = get_object_or_404(Flower, id=pk, owner=self.request.user)
            form = CreateForm(request.POST, request.FILES or None, instance=flower)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Autojust the model autos before saving
        flower = form.save(commit=False)
        flower.owner = self.request.user
        flower.save()
        return redirect(self.success_url)

class CommentCreateView(LoginRequiredMixin, View):
    template = 'flower_form.html'
    success_url = reverse_lazy('flowers')

    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk) :
        f = get_object_or_404(Flower, id=pk)
        comment_form = CommentForm(request.POST)

        comment = Comment(text=request.POST['comment'], owner=request.user, flower=f)
        comment.save()
        return redirect(reverse_lazy('flower_detail', args=[pk]))

class CommentDeleteView(FlowersDeleteView):
    model = Comment
    template_name = "flower_comment_delete.html"

    def get_success_url(self) :
        flower = self.object.flower
        return reverse_lazy('flower_detail', args=[flower.id])
