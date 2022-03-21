from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ArticleForm, ArticleDeleteForm
from webapp.models import Article
from webapp.views.base import SearchView


class IndexView(SearchView):
    model = Article
    context_object_name = "articles"
    template_name = "articles/index.html"
    paginate_by = 3
    paginate_orphans = 0
    search_fields = ["title__icontains", "author__icontains"]
    ordering=["-updated_at"]


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/create.html"
    permission_required = "webapp.add_article"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleView(DetailView):
    template_name = 'articles/view.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.object.comments.order_by("-created_at")
        context['comments'] = comments
        likes_connected = get_object_or_404(Article, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['number_of_likes'] = likes_connected.number_of_likes()
        context['post_is_liked'] = liked
        return context


def article_like(request, pk):
    post = get_object_or_404(Article, id=request.POST.get('article_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('webapp:article_view', args=[str(pk)]))


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "webapp.change_article"
    form_class = ArticleForm
    template_name = "articles/update.html"
    model = Article

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = "articles/delete.html"
    success_url = reverse_lazy('webapp:index')
    form_class = ArticleDeleteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "POST":
            kwargs['instance'] = self.object
        return kwargs
