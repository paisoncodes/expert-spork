from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.models import User
from accounts.permissions import IsCompanyAdminOrBaseAdmin, IsVerifiedAndActive
from notifications.models import Notification
from subscription.models import Invoice, Package, Subscription

from subscription.serializers import InvoiceSerializer, InvoiceViewSerializer, SubscriptionSerializer, SubscriptionViewSerializer

from utils.utils import api_response, send_mail
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from utils.query_params import customer_id



class AllSubscriptionsView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive, IsAdminUser]
    serializer_class = SubscriptionViewSerializer

    @swagger_auto_schema(operation_summary="View all subscriptions.")
    def get(self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionViewSerializer(subscriptions, many=True)
        return api_response("Subscriptions fetched", serializer.data, True, 200)
    
class SubscriptionView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = SubscriptionViewSerializer

    @swagger_auto_schema(manual_parameters=[customer_id], operation_summary="View Customer subscriptions")
    def get(self, request):
        if request.user.is_superuser:
            customer_id = request.GET.get("customer_id", None)
            if not customer_id:
                return api_response("Invalid customer", {}, False, 400)
            subscriptions = Subscription.objects.filter(customer__id=customer_id)
        else:
            subscriptions = Subscription.objects.filter(customer=request.user)
        serializer = SubscriptionViewSerializer(subscriptions, many=True)
        return api_response("Subscriptions fetched", serializer.data, True, 200)


class SubscriptionCreate(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive, IsAdminUser]
    serializer_class = SubscriptionSerializer

    @swagger_auto_schema(operation_summary="Create subscription.")
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            customer = serializer.data["customer"]
            user = User.objects.get(id=customer)
            Notification.objects.create(title="Subscription Added successfully.", user=user, object_id=serializer.data["id"])
            subject = "Subscription Added"

            message = "Subscription Added successfully"

            send_mail(user.email, subject=subject, body=message)
            return api_response("Subscription successful", serializer.data, True, 201)
        
        return api_response(serializer.errors, {}, False, 400)

class UserSubscriptionRetrieveView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = SubscriptionViewSerializer

    @swagger_auto_schema(operation_summary="View subscription.")
    def get(self, request, subscription_id):
        subscription = get_object_or_404(Subscription, id=subscription_id)
        serializer = self.serializer_class(subscription)
        return api_response("Subscription fetched", serializer.data, True, 200)
    
class UserSubscriptionUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive, IsAdminUser]
    serializer_class = SubscriptionSerializer

    @swagger_auto_schema(operation_summary="Update subscription.")
    def put(self, request, subscription_id):
        subscription = get_object_or_404(Subscription, id=subscription_id)
        serializer = self.serializer_class(request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=subscription, validated_data=serializer.validated_data)
            return api_response("Subscription Updated", serializer.data, True, 202)
        return api_response("ERROR", serializer.errors, False, 400)


# class PackageView(GenericAPIView):
#     permission_classes = [IsAuthenticated, IsVerifiedAndActive]
#     serializer_class = PackageSerializer

#     def get(self, request):
#         packages = Package.objects.filter(owner=request.user)
#         serializer = self.serializer_class(packages, many=True)
#         data = serializer.data
#         if invoice:= Invoice.objects.filter(subscription__id=data["id"]):
#             data["invoice"] = InvoiceViewSerializer(invoice).data
#         return api_response("Packages fetched", data, True, 200)
    
# class PackageCreateView(GenericAPIView):
#     permission_classes = [IsCompanyAdminOrBaseAdmin, IsVerifiedAndActive]
#     serializer_class = PackageSerializer

#     def post(self, request):
#         data = request.data 
#         data["owner"] = request.user
#         serializer = self.serializer_class(data)
#         if serializer.is_valid():
#             serializer.save()
#             return api_response("Package created", serializer.data, True, 201)

# class PackageRetrieveUpdateView(GenericAPIView):
#     permission_classes = [IsAuthenticated, IsVerifiedAndActive]
#     serializer_class = PackageSerializer

#     def get(self, request, package_id):
#         package = get_object_or_404(Package, id=package_id)
#         serializer = self.serializer_class(package)
#         return api_response("Package fetched", serializer.data, True, 200)

#     def put(self, request, package_id):
#         package, created = Package.objects.get_or_create(owner=request.user, id=package_id)
#         serializer = self.serializer_class(data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.update(instance=package, validated_data=serializer.validated_data)
#             return api_response("Package saved", serializer.data, True, 202)
#         return api_response(serializer.errors, {}, False, 400)
    
class InvoiceCreate(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive]
    serializer_class = InvoiceSerializer
    
    @swagger_auto_schema(operation_summary="Create invoice.")
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

    @swagger_auto_schema(operation_summary="View invoice.")
    def get(self, request, subscription_id):
        invoice = get_object_or_404(Invoice, subscription__id=subscription_id)
        serializer = self.serializer_class(invoice)
        return api_response("Invoices fetched", serializer.data, True, 200)

class InvoiceUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedAndActive, IsAdminUser]
    serializer_class = InvoiceViewSerializer

    @swagger_auto_schema(operation_summary="Update invoice.")
    def put(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        serializer = self.serializer_class(request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=invoice, validated_data=serializer.validated_data)
            return api_response("Invoice Updated", serializer.data, True, 202)
        return api_response("ERROR", serializer.errors, False, 400)