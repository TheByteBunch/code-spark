from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MatchRequest
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template import loader
from django.shortcuts import redirect

# Create your views here.


def login(request):
    return render(request, "login.html")


@login_required
def home(request):
    potential_match = get_potential_match(request.user)
    if potential_match:
        potential_match_message = "Your potential match is " + potential_match.username
    else:
        potential_match_message = (
            "No potential matches available. Please check back later"
        )
    context = {
        "potential_match_message": potential_match_message,
        "potential_match": potential_match,
    }
    template = loader.get_template("home.html")
    return HttpResponse(template.render(context, request))


# @login_required
# def match(request, other_requesting_user=None):
#     if other_requesting_user:
#         match_request = MatchRequest(match_request_sender)


@login_required
def request(request):
    user = request.user
    if MatchRequest.objects.filter(match_request_receiver=user).count() == 1:
        pass
        # TODO: redirect to match
    match_request = MatchRequest(
        match_request_sender=user,
        match_request_receiver=User.objects.get(username=request.GET["target-user"]),
        match_request_status=1,
        # do not set created_date or accepted date
    )
    match_request.save()
    # TODO: check for an existing matching match request_match. If found, will go to match, else go home
    return redirect("home")


@login_required
def decline(request):
    user = request.user
    # other_requesting_user = MatchRequest.objects.get(match_request_receiver=user)
    # matching_match_request = MatchRequest.objects.get(match_request_receiver=user)
    #     matching_match_request.
    match_request = MatchRequest(
        match_request_sender=user,
        match_request_receiver=User.objects.get(username=request.GET["target-user"]),
        match_request_status=-1,
        # do not set created_date or accepted date
    )
    match_request.save()
    # TODO: check for an existing matching match request_match. If found, will go to match, else go home
    return redirect("home")


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
        # .exclude(  # TODO: is this needed?
        #     sent_requests__match_request_receiver__username=user.username
        # )
        .exclude(username=user.username).values_list("pk", flat=True)
    )
    if len(pks) == 0:
        return None
    random_pk = choice(pks)
    potential_match = User.objects.get(pk=random_pk)

    return potential_match
