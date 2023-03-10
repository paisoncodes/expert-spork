from django.urls import path

from subscription.views import InvoiceRetrieveView, InvoiceView, PackageCreateView, PackageRetrieveUpdateView, PackageView, UserSubscriptionRetrieveView, SubscriptionView


urlpatterns = [
    path('subscription/', SubscriptionView.as_view()),
    path('subscription/view/', UserSubscriptionRetrieveView.as_view()),
    path('packages/all/', PackageView.as_view()),
    path('package/create/', PackageCreateView.as_view()),
    path("package/detail/<str:package_id>/", PackageRetrieveUpdateView.as_view()),
    path("invoices/", InvoiceView.as_view()),
    path("invoice/view/", InvoiceRetrieveView.as_view()),
]