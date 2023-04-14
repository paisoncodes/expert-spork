from django.urls import path

from subscription.views import AllSubscriptionsView, InvoiceCreate, InvoiceRetrieveView, InvoiceUpdateView, SubscriptionCreate, UserSubscriptionRetrieveView, SubscriptionView, UserSubscriptionUpdateView


urlpatterns = [
    path('subscription/', SubscriptionView.as_view()),
    path('subscription/create/', SubscriptionCreate.as_view()),
    path('subscription/view/', UserSubscriptionRetrieveView.as_view()),
    path('subscription/update/<str:subscription_id>/', UserSubscriptionUpdateView.as_view()),
    path("invoices/create/", InvoiceCreate.as_view()),
    path("invoice/view/<str:subscription_id>/", InvoiceRetrieveView.as_view()),
    path("invoice/update/<str:invoice_id>/", InvoiceUpdateView.as_view()),
    path("subscription/view/all/", AllSubscriptionsView.as_view())
]