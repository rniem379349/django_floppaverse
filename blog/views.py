from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from blog.forms import BlogPostForm, NewsletterSubscriptionForm
from blog.models import BlogPost
from users.models import Profile


class HomeView(ListView):
    model = BlogPost
    template_name = "blog/home.html"
    context_object_name = "blog_posts"
    paginate_by = 6
    site_title = "The latest blog posts"
    newsletter_form = NewsletterSubscriptionForm

    @cached_property
    def breadcrumbs(self):
        return {
            "Home": "",
            "Blog": reverse("blog:home"),
        }

    def get_queryset(self):
        return super().get_queryset().order_by("-created_timestamp")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "It's a blog"
        context["breadcrumbs"] = self.breadcrumbs
        context["site_title"] = self.site_title
        context["newsletter_form"] = self.newsletter_form
        return context


class PostDetailView(DetailView):
    model = BlogPost
    pk_url_kwarg = "blog_post_pk"
    context_object_name = "blog_post"
    template_name = "blog/blogpost_detail.html"

    @cached_property
    def breadcrumbs(self):
        return {
            "Home": "",
            "Blog": reverse("blog:home"),
            self.get_object().title: reverse(
                "blog:blog_post_detail", kwargs={"blog_post_pk": self.get_object().pk}
            ),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_post = self.get_object()
        context["title"] = f"{blog_post.title} | Blog"
        context["breadcrumbs"] = self.breadcrumbs
        return context


class PostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_create.html"
    site_title = "New Blog Post"
    success_url = reverse_lazy("blog:home")

    @cached_property
    def breadcrumbs(self):
        return {
            "Home": "",
            "Blog": reverse("blog:home"),
            "New Blog Post": reverse("blog:blog_post_create"),
        }

    def get_initial(self):
        initial = super().get_initial()
        initial["author"] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Blog Post"
        context["breadcrumbs"] = self.breadcrumbs
        context["site_title"] = self.site_title
        return context

    def form_valid(self, form):
        blog_post = form.save()
        messages.success(self.request, message="Blog Post created!")
        self.send_notification(blog_post=blog_post)
        return super().form_valid(form)

    def send_notification(self, blog_post):
        user = self.request.user
        post_title = blog_post.title
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications__broadcast",
            {
                "type": "notification",
                "chat_notification": False,
                "sent": now().strftime("%b %d, %Y, %H:%M"),
                "sender": user.pk,
                "sender_username": user.username,
                "sender_pic": user.profile.profile_pic.url,
                "message": f"{user} just posted a blog post! It's called {post_title}",
                "notification_url": blog_post.get_absolute_url(),
            },
        )


class PostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    pk_url_kwarg = "blog_post_pk"
    template_name = "blog/blogpost_create.html"
    site_title = "Edit Blog Post"

    @cached_property
    def breadcrumbs(self):
        return {
            "Home": "",
            "Blog": reverse("blog:home"),
            "Edit Blog Post": reverse(
                "blog:blog_post_update", kwargs={"blog_post_pk": self.get_object().pk}
            ),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Blog Post"
        context["breadcrumbs"] = self.breadcrumbs
        context["site_title"] = self.site_title
        return context

    def get_success_url(self):
        return reverse(
            "blog:blog_post_detail", kwargs={"blog_post_pk": self.get_object().pk}
        )

    def form_valid(self, form):
        messages.success(self.request, message="Blog Post updated successfully!")
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = BlogPost
    pk_url_kwarg = "blog_post_pk"
    site_title = "Delete Blog Post"
    success_url = reverse_lazy("blog:home")
    deleted_blog_post_name = ""

    def dispatch(self, request, *args, **kwargs):
        self.deleted_blog_post_name = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, message="Blog Post deleted successfully!")
        return super().form_valid(form)


class NewsletterSubscriptionCreateView(FormView):
    def post(self, request, *args, **kwargs):
        newsletter_form = NewsletterSubscriptionForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, message="Successfully subscribed to newsletter!")
            return HttpResponseRedirect(reverse("blog:home"))


class SearchResultsView(TemplateView):
    paginate_by = 10
    template_name = "blog/search.html"

    @cached_property
    def search_results(self):
        return self.get_search_results(self.request.GET.get("query"))

    @property
    def paginator(self):
        return Paginator(self.search_results, self.paginate_by)

    def get_search_results(self, query_str):
        if len(query_str) < 2:
            return {}
        blog_posts = BlogPost.objects.filter(title__icontains=query_str)
        users = Profile.objects.filter(user__username__icontains=query_str)
        return list(blog_posts) + list(users)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            results = self.paginator.page(self.request.GET.get("page", 1))
        except EmptyPage:
            results = self.paginator.page(self.paginator.num_pages)

        context["paginator"] = self.paginator
        context["page_obj"] = results
        context["search_query"] = self.request.GET.get("query")
        return context
