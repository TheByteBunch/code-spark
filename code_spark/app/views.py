from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MatchRequest
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template import loader
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout

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


@login_required
def match(request, match_request_id):
    """
    Takes a request which was redirected from /request,
    as well as a current_user (User) and a match_request
    (MatchRequest)

    :param request:
    :param current_user:
    :param match_request:
    :return:
    """
    match_request = get_object_or_404(MatchRequest, id=match_request_id)
    current_user = request.user

    if match_request.match_request_sender == current_user:
        other_user = match_request.match_request_receiver
    elif match_request.match_request_receiver == current_user:
        other_user = match_request.match_request_sender
    else:
        raise ValueError(
            f"Current user {current_user} should either be the match_request_sender "
            f"or the match_request_receiver of match_request {match_request}"
        )
    context = {
        "match_request": match_request,
        "current_user": current_user,
        "other_user": other_user,
    }
    return render(request, "match.html", context)


@login_required
def request(request):
    user = request.user
    if MatchRequest.objects.filter(match_request_receiver=user).count() == 1:
        match_request = MatchRequest.objects.get(match_request_receiver=user)
        match_request.match_request_receiver = user
        match_request.match_request_status = 2
        match_request.save()
        return redirect(
            "match",
            match_request_id=match_request.id,
        )
    match_request = MatchRequest(
        match_request_sender=user,
        match_request_receiver=User.objects.get(username=request.POST["target-user"]),
        match_request_status=1,
        # do not set created_date or accepted date
    )
    match_request.save()
    return redirect("home")


@login_required
def decline(request):
    user = request.user
    # other_requesting_user = MatchRequest.objects.get(match_request_receiver=user)
    # matching_match_request = MatchRequest.objects.get(match_request_receiver=user)
    #     matching_match_request.
    match_request = MatchRequest(
        match_request_sender=user,
        match_request_receiver=User.objects.get(username=request.POST["target-user"]),
        match_request_status=-1,
        # do not set created_date or accepted date
    )
    match_request.save()
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
        .exclude(
            sent_requests__match_request_receiver__username=user.username,
        )
        .exclude(username=user.username)
        .values_list("pk", flat=True)
    )
    pkslist = list(pks)
    pkslist.extend(
        MatchRequest.objects.filter(
            match_request_receiver__username=user.username, match_request_status=1
        ).values_list("match_request_sender__pk", flat=True)
    )

    if len(pkslist) == 0:
        return None
    random_pk = choice(pkslist)
    potential_match = User.objects.get(pk=random_pk)

    return potential_match


def get_matched_users(current_user):

    # Retrieve MatchRequest objects where the current user is involved and status is accepted
    matched_requests = MatchRequest.objects.filter(
        match_request_status=2,
        match_request_sender=current_user,
    ) | MatchRequest.objects.filter(
        match_request_status=2,
        match_request_receiver=current_user,
    )

    # Get the matched users from the MatchRequest objects
    matched_users = []
    for match_request in matched_requests:
        if match_request.match_request_sender == current_user:
            matched_users.append(match_request.match_request_receiver)
        else:
            matched_users.append(match_request.match_request_sender)

    return matched_users


@login_required
def matches(request):
    matched_users = get_matched_users(request.user)
    context = {"matched_users": matched_users}
    return render(request, "matches.html", context)


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()  # Delete the user account

        # Logout the user after deleting the account
        logout(request)

        return redirect("home")  # Redirect to a relevant page after account deletion
