from django.db import models
from accounts.models import BaseModel, User
from datetime import date, time

from accounts_profile.models import City, Lga, State



class IncidentType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
    
    @classmethod
    def get_default_pk(cls):
        name, created = cls.objects.get_or_create(
            name='default type',   
        )
        return created if created else name

class IncidentNature(models.Model):
    nature = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nature
    

class Incident(BaseModel):
    id = models.BigAutoField(primary_key=True, auto_created=True, serialize=False, verbose_name="ID")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=User.get_default_pk)
    name = models.CharField(max_length=225)
    incident_type = models.ForeignKey(IncidentType, on_delete=models.CASCADE, default=IncidentType.get_default_pk)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    lga = models.ForeignKey(Lga, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    # city = models.ForeignKey(City, on_delete=models.CASCADE)
    past_occurrences = models.JSONField(default=dict, null=True, blank=True)
    number_of_victims = models.IntegerField(default=0)
    special_events = models.TextField(blank=True, null=True)
    prior_warnings = models.TextField(blank=True, null =True)
    perpetrators = models.TextField(null=True, blank=True)
    incident_nature = models.ForeignKey(IncidentNature, on_delete=models.CASCADE)
    evidence = models.JSONField(default=dict, null=True, blank=True)
    company_approved = models.BooleanField(default=False)
    admin_approved = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.name
    

class Ticket(BaseModel):
    id = models.BigAutoField(primary_key=True, auto_created=True, serialize=False, verbose_name="ID")
    title = models.CharField(max_length=30, blank=True)
    message = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ticket_owner", blank=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    read = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

class TicketReply(BaseModel):
    id = models.BigAutoField(primary_key=True, auto_created=True, serialize=False, verbose_name="ID")
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    message = models.TextField(blank=True)
    read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.ticket.title

class TicketAssignee(BaseModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ticket_assignee")

    def __str__(self) -> str:
        return f"{self.assignee.email}:- {self.ticket.title}"
