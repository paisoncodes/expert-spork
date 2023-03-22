from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from accounts.models import User
from accounts.permissions import IsCompanyAdminOrBaseAdmin, IsVerifiedAndActive
from notifications.models import Notification
from subscription.models import Invoice, Package, Subscription

from subscription.serializers import InvoiceSerializer, InvoiceViewSerializer, PackageSerializer, SubscriptionSerializer, SubscriptionViewSerializer

from utils.utils import api_response
from django.shortcuts import get_object_or_404



class SubscriptionView(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsVerifiedAndActive]
    serializer_class = SubscriptionViewSerializer

    def get(self, request):
        subscriptions = Subscription.objects.filter(customer=request.user)
        serializer = SubscriptionViewSerializer(subscriptions, many=True)
        return api_response("Subscriptions fetched", serializer.data, True, 200)


class SubscriptionCreate(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsVerifiedAndActive]
    serializer_class = SubscriptionSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            customer = serializer.data["customer"]
            Notification.objects.create(title="Subscription Added successfully.", user=User.objects.get(id=customer), object_id=serializer.data["id"])
            return api_response("Subscription successful", serializer.data, True, 201)
        
        return api_response(serializer.errors, {}, False, 400)

class UserSubscriptionRetrieveView(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsVerifiedAndActive]
    serializer_class = SubscriptionViewSerializer

    def get(self, request):
        subscription = Subscription.objects.filter(customer=request.user).last()
        serializer = self.serializer_class(subscription)
        return api_response("Subscription fetched", serializer.data, True, 200)


class PackageView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = PackageSerializer

    def get(self, request):
        packages = Package.objects.filter(owner=request.user)
        serializer = self.serializer_class(packages, many=True)
        data = serializer.data
        if invoice:= Invoice.objects.filter(subscription__id=data["id"]):
            data["invoice"] = InvoiceViewSerializer(invoice).data
        return api_response("Packages fetched", data, True, 200)
    
class PackageCreateView(GenericAPIView):
    permission_classes = [IsCompanyAdminOrBaseAdmin, IsVerifiedAndActive]
    serializer_class = PackageSerializer

    def post(self, request):
        data = request.data 
        data["owner"] = request.user
        serializer = self.serializer_class(data)
        if serializer.is_valid():
            serializer.save()
            return api_response("Package created", serializer.data, True, 201)

class PackageRetrieveUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = PackageSerializer

    def get(self, request, package_id):
        package = get_object_or_404(Package, id=package_id)
        serializer = self.serializer_class(package)
        return api_response("Package fetched", serializer.data, True, 200)

    def put(self, request, package_id):
        package, created = Package.objects.get_or_create(owner=request.user, id=package_id)
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=package, validated_data=serializer.validated_data)
            return api_response("Package saved", serializer.data, True, 202)
        return api_response(serializer.errors, {}, False, 400)

class InvoiceView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = InvoiceViewSerializer

    def get(self, request):
        customer = request.GET.get("customer_id")
        invoices = Invoice.objects.all()
        if customer:
            invoices=invoices.filter(customer__id=customer)

        serializer = self.serializer_class(invoices, many=True)
        return api_response("Invoices fetched", serializer.data, True, 200)
    
class InvoiceCreate(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = InvoiceSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response("Invoices saved", serializer.data, True, 201)
        else:
            return api_response("Error", serializer.errors, False, 400)

class InvoiceRetrieveView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = InvoiceViewSerializer

    def get(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        serializer = self.serializer_class(invoice)
        return api_response("Invoice fetched", serializer.data, True, 200)