from django import forms

from blog.models import BlogPost, NewsletterSubscription


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = (
            "title",
            "content",
            "thumbnail",
            "author",
        )
        widgets = {
            "author": forms.HiddenInput(),
        }


class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ("email",)
