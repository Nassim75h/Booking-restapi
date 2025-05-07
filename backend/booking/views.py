from datetime import datetime
from django.core.validators import ValidationError
from django.db.models import Q
from django.views.generic import detail
from rest_framework.generics import get_object_or_404
import stripe
from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render, reverse
from rest_framework import (
    viewsets,
    status,
    permissions,
    mixins,
    filters,
)
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import viewsets
from booking.permissions import IsHostOrReadOnly
from booking.serializers import (
    BookingSerializer,
    CreateConversationSerializer,
    CreatePropertySerializer,
    PropertyImagesSerializer,
    PropertySerializer,
    ConversationSerializer,
    MessageSerializer,
)

from .models import Booking, Conversation, Property, PropertyImage, WaitListEntry, Message
from datetime import timedelta


class PropertyViewSet(ReadOnlyModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]  # Allow anyone to view properties

    def get_queryset(self):
        try:
            # Start with base queryset
            queryset = Property.objects.all()
            
            # Apply filters
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
                
            # Only return available properties
            queryset = queryset.filter(is_available=True)
                
            return queryset
            
        except Exception as e:
            print(f'Error in get_queryset: {str(e)}')
            return Property.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            
            if not queryset.exists():
                return Response(
                    {"message": "No properties found"},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            serializer = PropertySerializer(queryset, many=True, context={"request": self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": "Failed to fetch properties. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        print("\n=== Property Retrieve Debug ===")
        print(f"Request path: {request.path}")
        print(f"Request method: {request.method}")
        print(f"Request user: {request.user}")
        print(f"Request headers: {dict(request.headers)}")
        
        property_instance = self.get_object()
        serializer = PropertySerializer(property_instance,context={"request":self.request})
        data = serializer.data
        print(f"Serialized property: {data}")
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True,methods=['post','delete'])
    def add_to_wish_list(self,request,pk=None):
        print("\n=== Add to Wish List Debug ===")
        print(f"Request path: {request.path}")
        print(f"Request method: {request.method}")
        print(f"Request user: {request.user}")
        print(f"Request user authenticated: {request.user.is_authenticated}")
        print(f"Request headers: {dict(request.headers)}")
        print(f"Property ID: {pk}")
        print(f"Request data: {request.data}")
        
        try:
            property = self.get_object()
            print(f"Found property: {property.id}")
            user = request.user
            print(f"User: {user.id}")

            if request.method == "POST":
                existing_entry = WaitListEntry.objects.filter(guest=user, related_property=property).first()
                print(f"Existing entry: {existing_entry}")

                if existing_entry:
                    print("User is already in the waiting list")
                    return Response({"message": "You are already in the waiting list"},
                                    status=status.HTTP_400_BAD_REQUEST)
                
                try:
                    entry = WaitListEntry.objects.create(guest=user,
                                                  related_property=property)
                    print(f"Created new entry: {entry.id}")
                    return Response({"message": "Added to wishlist"},
                                    status=status.HTTP_201_CREATED)

                except ValidationError as e:
                    print(f"Validation error: {str(e)}")
                    return Response({"message":f"Error while adding to wishlist: {str(e)}"},
                                    status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    print(f"Unexpected error: {str(e)}")
                    return Response({"message": "An unexpected error occurred"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            elif request.method == "DELETE":
                entry = WaitListEntry.objects.filter(guest=user,related_property=property)
                if entry:
                    entry.delete()
                    print("Wait list canceled")
                    return Response({"message":"Waitlist canceled"},
                                    status=status.HTTP_204_NO_CONTENT)
                print("User is not in the wait list")
                return Response({"message":"You are not in the waitlist"},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error in add_to_wish_list: {str(e)}")
            return Response({"message": f"Error: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True,methods=["post"],url_path=r'confirm_wishlist/(?P<waitlist_entry_pk>\d+)')
    def confirm_wishlist(self,request,pk=None,waitlist_entry_pk=None):
        print("\n=== Confirm Wish List Debug ===")
        print(f"Request path: {request.path}")
        print(f"Request method: {request.method}")
        print(f"Request user: {request.user}")
        print(f"Request headers: {dict(request.headers)}")
        
        property=self.get_object()
        try: 
            entry =WaitListEntry.objects.get(id=waitlist_entry_pk,
                                             guest=request.user,
                                             related_property=property)
            if entry.confirmed :
                print("Already confirmed")
                return Response({"message":"You have already confirmed"},
                                    status=status.HTTP_400_BAD_REQUEST)
            entry.confirmed=True 
            entry.save()
            print("Booking confirmed")
            return Response({"message":"Booking confirmed "},
                                status=status.HTTP_200_OK)
        except ValidationError as e :
           print(f"Error while confirming the reservation: {str(e)}")
           return Response({"message":f"Error while confirming the reservation {str(e)}"},
                           status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='check_availability')
    def check_availability(self, request, pk=None):
        """
        Check if a property is available for the given dates
        """
        try:
            property_instance = self.get_object()
            check_in_date = request.query_params.get('check_in_date')
            check_out_date = request.query_params.get('check_out_date')

            if not check_in_date or not check_out_date:
                return Response({
                    'available': False,
                    'message': 'Both check-in and check-out dates are required'
                }, status=status.HTTP_200_OK)

            try:
                check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
                check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({
                    'available': False,
                    'message': 'Invalid date format. Use YYYY-MM-DD'
                }, status=status.HTTP_200_OK)

            if check_in >= check_out:
                return Response({
                    'available': False,
                    'message': 'Check-out date must be after check-in date'
                }, status=status.HTTP_200_OK)

            # Check if property is generally available
            if not property_instance.is_available:
                return Response({
                    'available': False,
                    'message': 'Property is not available for booking'
                }, status=status.HTTP_200_OK)

            # Check available_from and available_to dates
            if property_instance.available_from and check_in < property_instance.available_from.date():
                return Response({
                    'available': False,
                    'message': f'Property is only available from {property_instance.available_from.date()}'
                }, status=status.HTTP_200_OK)

            if property_instance.available_to and check_out > property_instance.available_to.date():
                return Response({
                    'available': False,
                    'message': f'Property is only available until {property_instance.available_to.date()}'
                }, status=status.HTTP_200_OK)

            # Check blocked dates
            if property_instance.blocked_dates:
                requested_dates = set(check_in + timedelta(days=x) for x in range((check_out - check_in).days))
                blocked_dates = set(datetime.strptime(date, '%Y-%m-%d').date() for date in property_instance.blocked_dates)
                if requested_dates.intersection(blocked_dates):
                    return Response({
                        'available': False,
                        'message': 'Some of the requested dates are blocked by the host'
                    }, status=status.HTTP_200_OK)

            # Check for overlapping bookings
            overlapping_bookings = Booking.objects.filter(
                property=property_instance,
                check_in_date__lt=check_out,
                check_out_date__gt=check_in,
                status__in=['CONFIRMED', 'PENDING']
            ).exists()

            if overlapping_bookings:
                return Response({
                    'available': False,
                    'message': 'Property is not available for these dates'
                }, status=status.HTTP_200_OK)

            # If we get here, the property is available
            return Response({
                'available': True,
                'message': 'Property is available for these dates'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'available': False,
                'message': f'Error checking availability: {str(e)}'
            }, status=status.HTTP_200_OK)


class OwnedPropertyViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsHostOrReadOnly]
    search_fields = ["title", "description"]
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        print("\n=== Owned Property Query Debug ===")
        print(f"Request path: {self.request.path}")
        print(f"Request method: {self.request.method}")
        print(f"Request user: {self.request.user}")
        print(f"Request headers: {dict(self.request.headers)}")
        
        return Property.objects.filter(host=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePropertySerializer
        return PropertySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    def list(self, request, *args, **kwargs):
        try:
            print("\n=== Owned Property List Debug ===")
            print(f"Request path: {request.path}")
            print(f"Request method: {request.method}")
            print(f"Request user: {request.user}")
            print(f"Request headers: {dict(request.headers)}")
            
            queryset = self.get_queryset()
            if not queryset.exists():
                print("You don't have any properties listed yet")
                return Response(
                    {"message": "You don't have any properties listed yet"},
                    status=status.HTTP_200_OK
                )
            serializer = self.get_serializer(queryset, many=True, context={'request': request})
            data = serializer.data
            print(f"Serialized {len(data)} properties")
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error in list view: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PropertyImageViewSet(ModelViewSet):
    serializer_class = PropertyImagesSerializer
    permission_classes = [IsAuthenticated, IsHostOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        return {
            "property_id": self.kwargs.get("property_pk"),
            "request": self.request
        }

    def get_queryset(self):
        print("\n=== Property Image Query Debug ===")
        print(f"Request path: {self.request.path}")
        print(f"Request method: {self.request.method}")
        print(f"Request user: {self.request.user}")
        print(f"Request headers: {dict(self.request.headers)}")
        
        property_id = self.kwargs.get("property_pk")
        if not property_id:
            return PropertyImage.objects.none()
        return PropertyImage.objects.filter(related_property_id=property_id)

    def perform_create(self, serializer):
        property_id = self.kwargs.get("property_pk")
        if not property_id:
            raise ValidationError("Property ID is required")

        try:
            property_instance = Property.objects.get(id=property_id)
            if property_instance.host != self.request.user:
                raise ValidationError("You can only upload images to your own properties")
        except Property.DoesNotExist:
            raise ValidationError("Property not found")

        serializer.save(related_property=property_instance)

    def create(self, request, *args, **kwargs):
        try:
            print("\n=== Property Image Create Debug ===")
            print(f"Request path: {request.path}")
            print(f"Request method: {request.method}")
            print(f"Request user: {request.user}")
            print(f"Request headers: {dict(request.headers)}")
            
            response = super().create(request, *args, **kwargs)
            return Response(
                {
                    "message": "Image uploaded successfully",
                    "data": response.data
                },
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            print(f"Error while uploading image: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(f"Failed to upload image: {str(e)}")
            return Response(
                {"error": "Failed to upload image. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print("\n=== Booking Query Debug ===")
        print(f"Request path: {self.request.path}")
        print(f"Request method: {self.request.method}")
        print(f"Request user: {self.request.user}")
        print(f"Request headers: {dict(self.request.headers)}")
        
        # For list action, return all user's bookings
        if self.action == 'list':
            return Booking.objects.filter(guest=self.request.user).select_related('property')
        
        # For other actions within a property context
        return Booking.objects.filter(guest=self.request.user)

    def get_serializer_context(self):
        context = {"user": self.request.user.id}
        if "property_pk" in self.kwargs:
            context["property_id"] = self.kwargs["property_pk"]
        return context

    def create(self, request, *args, **kwargs):
        print("\n=== Booking Create Debug ===")
        print(f"Request path: {request.path}")
        print(f"Request method: {request.method}")
        print(f"Request user: {request.user}")
        print(f"Request headers: {dict(request.headers)}")
        print(f"Request data: {request.data}")
        
        property_id = request.data.get('property')
        if not property_id:
            return Response(
                {"error": "Property ID is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BookingSerializer(
            data=request.data,
            context={
                "property_id": property_id,
                "user": request.user.id,
            },
        )
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            booking = serializer.save()
            
            property_obj = booking.property
            total_price = booking.total_price * 100
            YOUR_DOMAIN = request.build_absolute_uri("/")

            payment_method = request.data.get('payment_method', 'card')

            if payment_method == 'card':
                # Handle credit card payment through Stripe
                stripe.api_key = settings.STRIPE_KEY
                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[
                        {
                            "price_data": {
                                "currency": "dzd",  # Change to DZD for Algerian Dinar
                                "product_data": {
                                    "name": f"Booking for {property_obj}",
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
                return Response({
                    "id": booking.id,
                    "stripe_session_id": session.id,
                })
            elif payment_method == 'ccp':
                # Handle CCP Edahabia payment
                ccp_payment_url = f"https://edahabia.poste.dz/payment?amount={total_price}&reference={booking.id}"
                booking.payment_method = 'ccp'
                booking.save()
                return Response({
                    "id": booking.id,
                    "ccp_payment_url": ccp_payment_url
                })
            else:
                print("Invalid payment method")
                return Response(
                    {"error": "Invalid payment method"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(f"Error while creating booking: {str(e)}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StripePublicKeyView(APIView):
    def get(self, request, *args, **kwargs):
        print("\n=== Stripe Public Key Debug ===")
        print(f"Request path: {request.path}")
        print(f"Request method: {request.method}")
        print(f"Request user: {request.user}")
        print(f"Request headers: {dict(request.headers)}")
        
        # Fetch the Stripe public key from the settings
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        return Response({"stripe_public_key": stripe_public_key})


class CreateConversationViewset(ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = CreateConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"property_id": self.kwargs["property_pk"], "request": self.request}


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    @action(detail=True, methods=['post'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        
        if request.user not in conversation.participants.all():
            return Response(
                {"error": "You are not a participant in this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                conversation=conversation,
                sender=request.user
            )
            # Update the conversation's updated_at timestamp
            conversation.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        property_id = request.data.get('property_id')
        initial_message = request.data.get('initial_message')
        
        try:
            property_obj = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response(
                {"error": "Property not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create conversation
        conversation = Conversation.objects.create(property=property_obj)
        conversation.participants.add(request.user, property_obj.owner)
        
        # Add initial message if provided
        if initial_message:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=initial_message
            )
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def cancel(request):
    print("\n=== Cancel Debug ===")
    print(f"Request path: {request.path}")
    print(f"Request method: {request.method}")
    print(f"Request user: {request.user}")
    print(f"Request headers: {dict(request.headers)}")
    
    return render(request, "stripe/cancel.html")


def success(request):
    print("\n=== Success Debug ===")
    print(f"Request path: {request.path}")
    print(f"Request method: {request.method}")
    print(f"Request user: {request.user}")
    print(f"Request headers: {dict(request.headers)}")
    
    session_id = request.GET.get("session_id")
    if not session_id:
        print("Session Id missing")
        return HttpResponse("Session Id missing", status.HTTP_400_BAD_REQUEST)

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.StripeError as e:
        print(f"Error retrieving session: {str(e)}")
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
            print("Booking not found")
            return HttpResponse(
                "Booking not found ", status=status.HTTP_400_BAD_REQUEST
            )
    else:
        print("Payment not paid")
        return redirect("stripe-cancel")
    return render(request, "stripe/success.html")


class WishlistViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PropertySerializer

    def get_queryset(self):
        print("\n=== Wish List Query Debug ===")
        print(f"Request path: {self.request.path}")
        print(f"Request method: {self.request.method}")
        print(f"Request user: {self.request.user}")
        print(f"Request headers: {dict(self.request.headers)}")
        
        return Property.objects.filter(
            waitlistentry__guest=self.request.user
        ).prefetch_related('property')

    def list(self, request):
        print("\n=== Wish List Debug ===")
        print(f"Request path: {request.path}")
        print(f"Request method: {request.method}")
        print(f"Request user: {request.user}")
        print(f"Request headers: {dict(request.headers)}")
        
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        data = serializer.data
        print(f"Serialized {len(data)} properties")
        return Response(data)
