from datetime import datetime, timedelta
from django.db import models
from accounts.models import BaseModel, User
from accounts_profile.models import State
from incident.models import Advisory, AffectedGroup, AlertType, Impact, IncidentNature, PrimaryThreatActor, ThreatLevel
# Create your models here.


ACTIVE = "ACTIVE"
EXPIRED = "EXPIRED"
INVOICE = "INVOICE"
PAID = "PAID"
EMPTY = ""
class Package(BaseModel):
    name = models.CharField(max_length=20)
    description = models.TextField()
    price = models.FloatField(default=0)
    max_no_of_users = models.IntegerField(default=0)
    duration = models.IntegerField(default=1, help_text="Duration of the package in months")
    

    @classmethod
    def get_default_pk(cls):
        package, created = cls.objects.get_or_create(
            name='default package',  
            description = "Default package" 
        )
        return created if created else package
    
    def __str__(self) -> str:
        return self.name


class Subscription(models.Model):
    STATUSES = (
        (ACTIVE, ACTIVE), (EXPIRED, EXPIRED)
    )
    PAYMENT_STATUSES = (
        (EMPTY, EMPTY), (INVOICE, INVOICE), (PAID, PAID)
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    alert_type = models.ManyToManyField(AlertType, null=True)
    state = models.ManyToManyField(State, null=True)
    incident_nature = models.ManyToManyField(IncidentNature, null=True)
    primary_threat_actor = models.ManyToManyField(PrimaryThreatActor, null=True)
    impact = models.ManyToManyField(Impact, null=True)
    threat_level = models.ManyToManyField(ThreatLevel, null=True)
    affected_groups = models.ManyToManyField(AffectedGroup, null=True)
    number_of_users = models.IntegerField(default=1)
    amount = models.IntegerField(default=0)
    duration = models.IntegerField(default=1)
    expiry_date =  models.DateTimeField(null=True)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUSES, default=EMPTY)
    status = models.CharField(choices=STATUSES, max_length=50, default=ACTIVE)

    def __str__(self) -> str:
        return f"{self.customer.email} Security Incident Alert Service Subscription"

class Invoice(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(blank=True)
    paid = models.BooleanField(default=False)
    date_from = models.DateTimeField(blank=True)
    date_to = models.DateTimeField(blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    number_of_users = models.IntegerField(blank=True)
    invoice_number = models.TextField(blank=True)

    def save(self, *args, **kwargs) -> None:
        invoice_len = Invoice.objects.all().count()
        self.invoice_number = f"000{invoice_len}" if invoice_len < 10 else f"00{invoice_len}" if invoice_len < 100 else f"0{invoice_len}" if invoice_len < 1000 else invoice_len
        if self.payment_date:
            self.paid = True
            self.subscription.payment_status=PAID
        else:
            self.subscription.payment_status=INVOICE
        if self.subscription:
            self.date_to= self.subscription.expiry_date
            self.date_from = self.date_to - timedelta(days=(self.subscription.duration*30))
            self.amount=self.subscription.amount
            self.number_of_users = self.subscription.number_of_users
        else:
            self.date_from = self.date_to= datetime.today()
            self.amount = self.number_of_users = 0
        return super().save( *args, **kwargs)

