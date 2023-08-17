from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MatchRequest
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template import loader

# Create your views here.

def login(request):
    return render(request, 'login.html')

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
    potential_match = (User.objects.
                       exclude(received_requests__match_request_sender__username
                                                     =user.username)
                       .exclude(username=user.username)
                       [0]
    )
        # received_requests__match_requst_sender__user=user)

    # Blog.objects.filter(entry__headline__contains="Lennon")
    #.exclude(matchrequest__match_request_receiver=user)
            # .order_by(user.username)[0])

    return potential_match