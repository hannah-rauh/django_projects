from ads.models import Ad, Comment, Fav

from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse

from django.core.files.uploadedfile import InMemoryUploadedFile

from ads.util import AdsListView, AdsDetailView, AdsCreateView, AdsUpdateView, AdsDeleteView

from ads.forms import CreateForm, CommentForm

class AdListView(AdsListView):
    model = Ad
    template_name = "ad_list.html"

    def get(self, request) :
        ad_list = Ad.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}]  (A list of rows)
            rows = request.user.favorite_ads.values('id')
            favorites = [ row['id'] for row in rows ]
        ctx = {'ad_list' : ad_list, 'favorites': favorites}
        return render(request, self.template_name, ctx)



class AdDetailView(AdsDetailView):
    model = Ad
    template_name = "ad_detail.html"
    def get(self, request, pk) :
        ad = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : ad, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)


# class AdCreateView(AdsCreateView):
#     model = Ad
#     fields = ['title', 'text', 'price']
#     template_name = "ad_form.html"
#     success_url = reverse_lazy('ads')
#     def get(self, request, pk=None) :
#         form = CreateForm()
#         ctx = { 'form': form }
#         return render(request, self.template, ctx)
#
#     def post(self, request, pk=None) :
#         form = CreateForm(request.POST, request.FILES or None)
#
#         if not form.is_valid() :
#             ctx = {'form' : form}
#             return render(request, self.template, ctx)
#
#         # Add ads to the model before saving
#         ad = form.save(commit=False)
#         ad.owner = self.request.user
#         ad.save()
#         return redirect(self.success_url)
#
#
# class AdUpdateView(AdsUpdateView):
#     model = Ad
#     fields = ['title', 'text', 'price']
#     template = "ad_form.html"
#     success_url = reverse_lazy('ads')
#     def get(self, request, pk) :
#         ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
#         form = CreateForm(instance=ad)
#         ctx = { 'form': form }
#         return render(request, self.template, ctx)
#
#     def post(self, request, pk=None) :
#         ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
#         form = CreateForm(request.POST, request.FILES or None, instance=ad)
#
#         if not form.is_valid() :
#             ctx = {'form' : form}
#             return render(request, self.template, ctx)

class AdDeleteView(AdsDeleteView):
    model = Ad
    template_name = "ad_delete.html"

def stream_file(request, pk) :
    pic = get_object_or_404(Ad, id=pk)
    print(id)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response


class AdFormView(LoginRequiredMixin, View):
    model= Ad
    template = 'ad_form.html'
    success_url = reverse_lazy('ads')
    def get(self, request, pk=None) :
        if not pk :
            form = CreateForm()
        else:
            pic = get_object_or_404(Ad, id=pk, owner=self.request.user)
            form = CreateForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            pic = get_object_or_404(Ad, id=pk, owner=self.request.user) #looking for an object in the model
            form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Adjust the model owner before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)




class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment_form = CommentForm(request.POST)

        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        return redirect(reverse_lazy('ad_detail', args=[pk]))

class CommentDeleteView(AdsDeleteView):
    model = Comment
    template_name = "comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        ad = self.object.ad
        return reverse_lazy('ad_detail', args=[ad.id])


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, ad=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()
