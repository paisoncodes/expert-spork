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

class AlertType(models.Model):
    name = models.CharField(max_length=40)
    definition = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    

class PrimaryThreatActor(models.Model):
    name = models.CharField(max_length=40)
    definition = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    

class Impact(models.Model):
    name = models.CharField(max_length=40)
    definition = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    

class AffectedGroup(models.Model):
    name = models.CharField(max_length=40)
    definition = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Advisory(models.Model):
    name = models.CharField(max_length=40)
    definition = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    

class ThreatLevel(models.Model):
    name = models.CharField(max_length=40)
    color_code = models.CharField(max_length=20)
    definition = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    

class Incident(BaseModel):
    id = models.BigAutoField(primary_key=True, auto_created=True, serialize=False, verbose_name="ID")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=User.get_default_pk)
    alert_type = models.ForeignKey(AlertType, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    incident_nature = models.ForeignKey(IncidentNature, on_delete=models.CASCADE)
    threat_level = models.ForeignKey(ThreatLevel, on_delete=models.SET_NULL, null=True, blank=True)
    impact = models.ForeignKey(Impact, on_delete=models.SET_NULL, null=True, blank=True)
    primary_threat_actor = models.ForeignKey(PrimaryThreatActor, on_delete=models.SET_NULL, null=True, blank=True)
    affected_groups = models.ManyToManyField(AffectedGroup)
    details = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=225, default=str)
    lga = models.ForeignKey(Lga, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    # city = models.ForeignKey(City, on_delete=models.CASCADE)
    past_occurrences = models.TextField(null=True, blank=True)
    number_of_victims = models.IntegerField(default=0)
    special_events = models.TextField(blank=True, null=True)
    prior_warnings = models.TextField(blank=True, null =True)
    evidence = models.JSONField(default=dict, null=True, blank=True)
    company_approved = models.BooleanField(default=False)
    admin_approved = models.BooleanField(default=False)
    advisory = models.TextField(null=True, blank=True)


    def __str__(self) -> str:
        return self.alert_type.name
    

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
