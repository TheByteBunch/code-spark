from django.db import models
from django.contrib.auth.models import User


class MatchRequest(models.Model):
    match_request_sender = models.ForeignKey(
        User, related_name="sent_requests", on_delete=models.CASCADE
    )
    match_request_receiver = models.ForeignKey(
        User, related_name="received_requests", on_delete=models.CASCADE
    )
    match_request_status = (
        models.IntegerField()
    )  # 1 is request_match sent, -1 is sender declined, 2 is receiver accepted, -2 is receiver declined.
    created_date = models.DateTimeField(auto_now_add=True)
    accepted_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.match_request_sender} to {self.match_request_receiver}"
