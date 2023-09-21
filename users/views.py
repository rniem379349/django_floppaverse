from functools import cached_property

from django.contrib import messages
from django.contrib.auth import views
from django.contrib.auth.mixins import (
    AccessMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from users.filters import ProfileFilter
from users.forms import (
    ProfileUpdateForm,
    UserRegisterForm,
    UserReportForm,
    UserUpdateForm,
)
from users.models import Profile, UserReport


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sign up | bloggodoggo"
        return context

    def get_success_url(self):
        return reverse("blog:home")

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        return form_kwargs

    def form_valid(self, form, *args, **kwargs):
        username = form.cleaned_data.get("username", "user")
        user = form.save()
        profile = Profile(user=user)
        profile.save()
        messages.success(
            self.request, message="Account created, welcome, {}!".format(username)
        )
        return super(RegisterView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.warning(
            self.request,
            message="There were some errors with your registration."
            " Please check the error messages below.",
        )
        return super(RegisterView, self).form_invalid(form, *args, **kwargs)


class LoginView(views.LoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        user = form.get_user()
        messages.success(
            self.request, message="Logged in successfully. Welcome, {}!".format(user)
        )
        return super().form_valid(form)


class LogoutView(views.LogoutView):
    user_logging_out = ""

    def dispatch(self, request, *args, **kwargs):
        self.user_logging_out = request.user.username
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages.success(
            self.request,
            message="Logged out successfully. Until next time, {}!".format(
                self.user_logging_out
            ),
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("blog:home")


class UserUpdateView(UserPassesTestMixin, AccessMixin, TemplateView):
    template_name = "users/profile_edit.html"
    user_form_class = UserUpdateForm
    profile_form_class = ProfileUpdateForm

    def test_func(self):
        target_user = User.objects.get(pk=self.kwargs.get("user_pk"))
        return self.request.user == target_user

    def get_user_form(self, post_data, user_instance=None):
        return self.user_form_class(post_data, instance=user_instance, prefix="user")

    def get_profile_form(self, post_data, profile_instance=None):
        return self.profile_form_class(
            post_data, self.request.FILES, instance=profile_instance, prefix="profile"
        )

    def post(self, request, *args, **kwargs):
        post_data = request.POST or None
        user_instance = User.objects.get(pk=kwargs.get("user_pk"))
        profile_instance = user_instance.profile
        user_form = self.get_user_form(post_data, user_instance=user_instance)
        profile_form = self.get_profile_form(
            post_data, profile_instance=profile_instance
        )

        context = self.get_context_data(user_form=user_form, profile_form=profile_form)

        if user_form.is_valid():
            user_form.save()
        if profile_form.is_valid():
            profile_form.save()

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class UserProfileDetailView(DetailView):
    template_name = "users/profile.html"
    model = User
    pk_url_kwarg = "user_pk"
    context_object_name = "shown_user"

    @cached_property
    def breadcrumbs(self):
        return {
            "Home": "",
            "User List": reverse("users:user_list"),
            "Profile": reverse("users:profile", kwargs={"user_pk": self.object.pk}),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self.breadcrumbs
        return context


class UserListView(ListView):
    template_name = "users/profile_list.html"
    model = Profile
    context_object_name = "user_list"
    paginate_by = 3
    site_title = "User List"

    @cached_property
    def breadcrumbs(self):
        return {
            "Home": "",
            "User List": reverse("users:user_list"),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self.breadcrumbs
        context["site_title"] = self.site_title
        context["filter"] = ProfileFilter(self.request.GET, queryset=self.queryset)
        context["get_params"] = self.request.GET.copy()
        return context

    def get_queryset(self):
        return ProfileFilter().qs


class UserReportView(PermissionRequiredMixin, AccessMixin, CreateView):
    permission_required = "users.add_userreport"
    template_name = "users/profile_report_create.html"
    pk_url_kwarg = "user_pk"
    model = UserReport
    form_class = UserReportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["target_user"] = self.get_target_user()
        return context

    def get_target_user(self):
        return User.objects.get(pk=self.kwargs.get("user_pk"))

    def get_initial(self):
        initial = super().get_initial()
        initial["target_user"] = self.get_target_user()
        initial["author"] = self.request.user
        return initial

    def get_success_url(self):
        return reverse("users:profile", kwargs={"user_pk": self.get_target_user().pk})

    def form_valid(self, form):
        super().form_valid(form)
        messages.success(
            self.request,
            message="Report sent (reference number {}). If you supplied a contact email, \
            we will get in touch with you once the report has been processed.".format(
                self.object.pk
            ),
        )
        return HttpResponseRedirect(self.get_success_url())
