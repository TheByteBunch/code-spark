from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MatchRequest
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template import loader

# Create your views here.


def login(request):
    return render(request, "login.html")


@login_required
def home(request):
    context = {"potential_match": get_potential_match(request.user)}
    template = loader.get_template("home.html")
    return HttpResponse(template.render(context, request))


def get_potential_match(user):
    """
    Returns a user that the current user has not been seen by and
    has not seen.
    :param user:
    :return:
    """

    from random import choice

    pks = (
        User.objects.exclude(
            received_requests__match_request_sender__username=user.username
        )
        .exclude(username=user.username)
        .values_list("pk", flat=True)
    )
    random_pk = choice(pks)
    potential_match = User.objects.get(pk=random_pk)

    return potential_match
