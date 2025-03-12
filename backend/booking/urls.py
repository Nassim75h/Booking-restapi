from rest_framework import routers
from rest_framework_nested import routers
from django.urls import include, path
from . import views

router = routers.DefaultRouter()
router.register(r'owned-property', views.OwnedPropertyViewSet, basename='owned-properties')
router.register(r'properties',views.PropertyViewSet,basename='properties')

owned_rooms=routers.NestedDefaultRouter(
            router,'owned-property',lookup='property')

owned_rooms.register(r'images',views.PropertyImageViewSet,basename='property-images')




property_router = routers.NestedDefaultRouter(
    router, 'properties', lookup='property')

property_router.register(
    r'images', views.PropertyImageViewSet, basename='property-images')
property_router.register(
    r'book',views.BookingViewSet,basename='property-bookings')
property_router.register(r'create_conversation',views.CreateConversationViewset,basename='converstion')



urlpatterns =[
    path('',include(owned_rooms.urls)),
    path('',include(router.urls)),
    path('public-key/', views.StripePublicKeyView.as_view(), name='stripe-public-key'),
    path('',include(property_router.urls)),
    path('stripe/success/',views.success,name='stripe-success'),
    path('stripe/cancel/',views.cancel,name='stripe-cancel'),

]
