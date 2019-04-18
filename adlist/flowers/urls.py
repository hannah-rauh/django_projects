from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.FlowerListView.as_view()),
    path('flowers', views.FlowerListView.as_view(), name='flowers'),
    path('flower/<int:pk>', views.FlowerDetailView.as_view(), name='flower_detail'),
    path('flower/create',
        views.FlowerFormView.as_view(success_url=reverse_lazy('flowers')), name='flower_create'),
    path('flower/<int:pk>/update',
        views.FlowerFormView.as_view(success_url=reverse_lazy('flowers')), name='flower_update'),
    path('flower/<int:pk>/delete',
        views.FlowerDeleteView.as_view(success_url=reverse_lazy('flowers')), name='flower_delete'),
    path('ad/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='flower_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('ads')), name='flower_comment_delete'),
]
