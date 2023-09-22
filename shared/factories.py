import factory
from django.contrib.auth.models import User
from django.utils import timezone

from users.models import Profile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "john%s" % n)
    first_name = "John"
    last_name = "Doe"
    email = factory.LazyAttribute(lambda o: "%s@example.org" % o.username)
    date_joined = factory.LazyFunction(timezone.now)


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    profile_pic = factory.django.ImageField(color="blue")
