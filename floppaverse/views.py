from django.urls import reverse
from django.views.generic import RedirectView


class HomePageRedirectView(RedirectView):
    def get_redirect_url(self):
        return reverse("blog:home")
