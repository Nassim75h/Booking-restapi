from datetime import datetime
from django.core.validators import ValidationError
from django.views.generic import detail
from rest_framework.generics import get_object_or_404
import stripe
from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render, reverse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from booking.permissions import IsHostOrReadOnly
from booking.serializers import (
    BookingSerializer,
    CreateConversationSerializer,
    CreatePropertySerializer,
    PropertyImagesSerializer,
    PropertySerializer,
)

from .models import Booking, Conversation, Property, PropertyImage, WaitListEntry


class PropertyViewSet(ReadOnlyModelViewSet):
    serializer_class = PropertySerializer

    def get_queryset(self):
        queryset = Property.objects.prefetch_related("property").all()
        category = self.request.query_params.get("category")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        max_guests = self.request.query_params.get("max_guests")
        if max_guests:
            queryset = queryset.filter(max_guests__lte=max_guests)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PropertySerializer(queryset, many=True,context={"request":self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        property_instance = self.get_object()
        serializer = PropertySerializer(property_instance,context={"request":self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True,methods=['post','delete'])
    def add_to_wish_list(self,request,pk=None):
        property=self.get_object()
        user=request.user
        if request.method == "POST" :

            if WaitListEntry.objects.filter(guest=user,related_property=property).first() :
                return Response({"message": "you are already in the waiting list"},
                                status=status.HTTP_403_FORBIDDEN)
            try:

                WaitListEntry.objects.create(guest=user,
                                             related_property=property)
                return Response({"message":"added to wishlsit"},
                                status=status.HTTP_200_OK)

            except ValidationError as e:
                return Response({"message":f"error while adding to wishlist {str(e)}"},
                                status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            entry =WaitListEntry.objects.filter(guest=user,related_property=property)
            if entry :
                entry.delete()
                return Response({"message":"wailist canceled "},
                                status=status.HTTP_204_NO_CONTENT)
            return Response({"message":" your arenot in the waitlist"},
                            status=status.HTTP_404_NOT_FOUND) 


    @action(detail=True,methods=["post"],url_path=r'confirm_wishlist/(?P<waitlist_entry_pk>\d+)')
    def confirm_wishlist(self,request,pk=None,waitlist_entry_pk=None):
        property=self.get_object()
        try: 
            entry =WaitListEntry.objects.get(id=waitlist_entry_pk,
                                             guest=request.user,
                                             related_property=property)
            if entry.confirmed :
                return Response({"message":"You have already confirmed"},
                                    status=status.HTTP_400_BAD_REQUEST)
            entry.confirmed=True 
            entry.save()
            return Response({"mesage":"Booking confirmed "},
                                status=status.HTTP_200_OK)
        except ValidationError as e :
           return Response({"message":f"error while confirming the reservation {str(e)}"},
                           status=status.HTTP_400_BAD_REQUEST)

class OwnedPropertyViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsHostOrReadOnly]
    search_fields = ["title", "description"]

    @action(detail=True, methods=["post"])
    def add_blocked_dates(self, request):
        property = self.get_object()
        blocked_dates = request.data.get("blocked_dates")

        if not isinstance(blocked_dates, list):
            return Response(
                {"detail": "The blocked_dates field must be list of dates."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invalid_dates = []
        for date_str in blocked_dates:
            try:
                blocked_date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                if str(blocked_date_obj) not in property.blocked_dates:
                    property.blocked_dates.append(str(blocked_date_obj))
                else:
                    invalid_dates.append(date_str)
            except ValueError:
                invalid_dates.append(date_str)
        if invalid_dates:
            return Response(
                {
                    "detail": f"Invalid date(e) or already exist : {', '.join(invalid_dates)}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        property.save()
        return Response(
            {"detail": "Blocked date(s) added successfully"}, status=status.HTTP_200_OK
        )

    def get_queryset(self):
        return Property.objects.prefetch_related("property").filter(
            host=self.request.user
        )

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH", "POST"]:
            return CreatePropertySerializer
        return PropertySerializer

    # NOTE this function to add host id directly when creating a property item
    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class PropertyImageViewSet(ModelViewSet):
    serializer_class = PropertyImagesSerializer
    permission_classes = [IsAuthenticated, IsHostOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        return {"property_id": self.kwargs["property_pk"], "request": self.request}

    def get_queryset(self):
        return PropertyImage.objects.filter(
            related_property_id=self.kwargs["property_pk"],
        )

    def perform_create(self, serializer):
        serializer.save(related_property_id=self.kwargs.get("property_pk"))


class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user)

    def get_serializer_context(self):
        return {"property_id": self.kwargs["property_pk"], "user": self.request.user.id}

    def create(self, request, *args, **kwargs):

        stripe.api_key = settings.STRIPE_KEY
        serializer = BookingSerializer(
            data=request.data,
            context={
                "property_id": self.kwargs["property_pk"],
                "user": self.request.user.id,
            },
        )
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        property = serializer.validated_data.get("property")
        total_price = booking.total_price * 100
        YOUR_DOMAIN = request.build_absolute_uri("/")  # Get the domain dynamically

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": f"Booking for {property}",
                            },
                            "unit_amount": int(total_price),
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=f'{YOUR_DOMAIN}{reverse("stripe-success")}?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=f'{YOUR_DOMAIN}{reverse("stripe-cancel")}',
            )
            booking.stripe_session_id = session.id
            booking.save()
            return Response(
                {
                    "id": booking.id,
                    "sessionId": session.id,
                }
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StripePublicKeyView(APIView):
    def get(self, request, *args, **kwargs):
        # Fetch the Stripe public key from the settings
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        return Response({"stripe_public_key": stripe_public_key})


class CreateConversationViewset(ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = CreateConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"property_id": self.kwargs["property_pk"], "request": self.request}


def cancel(request):
    return render(request, "stripe/cancel.html")


def success(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return HttpResponse("Session Id missing", status.HTTP_400_BAD_REQUEST)

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.StripeError as e:
        return HttpResponse(
            f"Error retrieving sesison:{str(e)}",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if session.payment_status == "paid":
        try:
            booking = Booking.objects.get(stripe_session_id=session.id)
            booking.is_paid = True
            booking.save()
        except Booking.DoesNotExist:
            return HttpResponse(
                "Booking not found ", status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return redirect("stripe-cancel")
    return render(request, "stripe/success.html")




