from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from accounts.permissions import IsCompanyAdminOrBaseAdmin
from subscription.models import Package, Subscription

from subscription.serializers import PackageSerializer, SubscriptionSerializer

from utils.utils import api_response
from django.shortcuts import get_object_or_404



class SubscriptionView(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SubscriptionSerializer

    def get(self, request):
        subscription = Subscription.objects.filter(user=request.user).first()
        serializer = self.serializer_class(subscription)
        return api_response("Subscription fetched", serializer.data, True, 200)

    def post(self, request):
        data = request.data
        data["user"] = request.user
        serializer = self.serializer_class(data)
        if serializer.is_valid():
            serializer.save()
            package = serializer.package
            package.no_of_subscribers += 1
            package.save()
            return api_response("Subscription successful", serializer.data, True, 201)
        
        return api_response(serializer.errors, {}, False, 400)

    def put(self, request):
        subscription, created = Subscription.objects.get_or_create(user=request.user)
        serializer = self.serializer_class(data=subscription, partial=True)
        if serializer.is_valid():
            serializer.update(instance=subscription, validated_data=serializer.validated_data)
            return api_response("Subscription updated", serializer.data, True, 202)
        return api_response(serializer.errors, {}, False, 400)


class PackageView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PackageSerializer

    def get(self, request):
        packages = Package.objects.filter(owner=request.user)
        serializer = self.serializer_class(packages, many=True)
        return api_response("Packages fetched", serializer.data, True, 200)
    
class PackageCreateView(GenericAPIView):
    permission_classes = [IsCompanyAdminOrBaseAdmin]
    serializer_class = PackageSerializer

    def post(self, request):
        data = request.data 
        data["owner"] = request.user
        serializer = self.serializer_class(data)
        if serializer.is_valid():
            serializer.save()
            return api_response("Package created", serializer.data, True, 201)

class PackageRetrieveUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated,]
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