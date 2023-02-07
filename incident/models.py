from django.db import models
from accounts.models import BaseModel, User
from datetime import date, time


class Incident(BaseModel):
    id = models.BigAutoField(primary_key=True, auto_created=True, serialize=False, verbose_name="ID")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=User.get_default_pk)
    name = models.CharField(max_length=225)
    incident_type = models.CharField(max_length=225)
    date = models.DateField()
    time = models.TimeField()
    details = models.TextField()
    location = models.CharField(max_length=500)
    past_occurrences = models.JSONField(default=dict)
    number_of_victims = models.IntegerField(default=0)
    special_events = models.TextField()
    prior_warnings = models.TextField()
    perpetrators = models.TextField()
    nature_of_incident = models.CharField(max_length=100)
    evidence = models.JSONField(default=dict)
    

class Ticket(BaseModel):
    id = models.BigAutoField(primary_key=True, auto_created=True, serialize=False, verbose_name="ID")
    title = models.CharField(max_length=30)
    message = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)

class TicketReply(BaseModel):
    id = models.BigAutoField(primary_key=True, auto_created=True, serialize=False, verbose_name="ID")
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
