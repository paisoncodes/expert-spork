from django.urls import path

from subscription.views import PackageCreateView, PackageRetrieveUpdateView, PackageView, SubscriptionView


urlpatterns = [
    path('subscription/', SubscriptionView.as_view()),
    path('packages/all/', PackageView.as_view()),
    path('package/create/', PackageCreateView.as_view()),
    path("package/detail/<str:package_id>/", PackageRetrieveUpdateView.as_view()),
]