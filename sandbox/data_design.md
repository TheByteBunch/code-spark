# Data Design

In order to show a user a new profile from another user, the app needs to know:
- what other users the currently logged in user has already seen (and reacted to)
- What users are signed up for the app overall

It turns out, the current data design, which I lifted from a tinder clone tutorial website,
is sufficient to hold this information.

We will just need to do a search of the database model MatchRequest, with
match_request_sender equal to current user or match_request_receiver equal to 
current user.
These are the profiles we should not show to the user.
Then we search in the users database, with the condition that username not equal
the usernames found in the previous step.

Also, here is more commentary on the MatchRequest datatype.

Currently in the models file:
```py
match_request_status = models.IntegerField()  # 0 is requested, 1 is accepted, -1 is rejected
created_date = models.DateTimeField(auto_now_add=True)
accepted_date = models.DateTimeField(null=True, blank=True)
```

I want to adjust the codes in match_request_status
0 would be unseen, except in that case there will be no entry in the database at all
1 will be request sent, it means user who was presented with the potential match first will 
have clicked yes or "swiped right" on the other user.
-1 will be rejected. It means the user who was presented with the potential match said no 
or "swiped left" on the other user.
(side note: will it be possible to have a record with usera as sender rejecting userb as potential 
receiver, and a separate record with userb as sender rejecting user a as a potential receiver. 
Let's say no. Becuase if userA rejected userB, let's just not show userA to userB.)  
Summary of status codes for match_request_status: 1 is request sent, -1 is sender declined, 2 is receiver accepted, -2 is receiver declined.

Let's go and update the model code



side note: do I want a uuid for user IDs, or is it enough to just use the github username.
I think for now, github username will do. But maybe later I will add a uuid.