from authapp.models import User
from rest_framework import serializers
from . import models

class PropertyImagesSerializer(serializers.ModelSerializer):
    images=serializers.ListField(
            child=serializers.ImageField(),
            required=False)
    class Meta:
        model = models.PropertyImage
        fields = ["id",'image','images']

    def get_image_url(self, obj):
        request=self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def create(self, validated_data):
        property_id = self.context.get("property_id")

        if not property_id:
            raise serializers.ValidationError("property_id must be provided")
        try:
            related_property = models.Property.objects.get(id=property_id)
        except models.Property.DoesNotExist:
            raise serializers.ValidationError(f"property with id {property_id} does not exist")

        # Handle both single image and multiple images
        single_image = validated_data.get('image')
        multiple_images = validated_data.get('images', [])

        if single_image:
            # Create a single image
            return models.PropertyImage.objects.create(
                related_property=related_property,
                image=single_image
            )
        elif multiple_images:
            # Create multiple images
            property_images = [
                models.PropertyImage(related_property=related_property, image=image)
                for image in multiple_images
            ]
            created_images = models.PropertyImage.objects.bulk_create(property_images)
            if not created_images:
                raise serializers.ValidationError("No images were created")
            return created_images[0]
        else:
            raise serializers.ValidationError("No image provided")


    def update(self, instance, validated_data):
        property_id = self.context.get("property_id")
        if not property_id:
            raise serializers.ValidationError("Property ID must be provided.")

        try:
            related_property = models.Property.objects.get(id=property_id)
        except models.Property.DoesNotExist:
            raise serializers.ValidationError(
                f"Property with id {property_id} doesnt exist"
            )

        instance.related_property = related_property
        instance.image = validated_data.get("image", instance.image)
        instance.save()
        return instance


class CreatePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Property
        fields = [
            "id",
            "title",
            "city",
            "address",
            "price_per_night",
            "max_guests",
            "description",
            "category",
            "host"
        ]
        read_only_fields = ["host"]
    
    def validate_price_per_night(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate_max_guests(self, value):
        if value <= 0:
            raise serializers.ValidationError("Maximum guests must be greater than 0")
        return value

    def create(self, validated_data):
        # Get the user from the context
        user = self.context.get('request').user
        validated_data['host'] = user
        return super().create(validated_data)


class PropertySerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    host = serializers.SerializerMethodField()
    description = serializers.CharField(required=False)
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = models.Property
        fields = [
            "id",
            "title",
            "host",
            "address",
            "city",
            "category",
            "max_guests",
            "price_per_night",
            "description",
            "images",
            "blocked_dates",
            "is_available"
        ]

    def get_host(self,obj):
        return {
            "id":obj.host.id,
            "username":obj.host.username
        }
        
    def get_images(self, obj):
        request = self.context.get('request')
        images = []
        for image in obj.images.all():
            if image.image:
                if request:
                    image_url = request.build_absolute_uri(image.image.url)
                else:
                    image_url = image.image.url
                images.append(image_url)
        return images


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Booking
        fields=['id','property','guest','check_in_date','check_out_date',
        'total_price','status','stripe_session_id','is_paid']
        read_only_fields=['guest','property','total_price','status','stripe_session_id','is_paid']

    def validate(self, attrs):
        property_instance=self.context.get('property_id')
        check_in_date=attrs['check_in_date']
        check_out_date=attrs['check_out_date']
        overlapping_bookings=models.Booking.objects.filter(
                property=property_instance,
                check_in_date__lte=check_out_date,
                check_out_date__gt=check_in_date
        )
                

        if check_out_date<=check_in_date:
            raise serializers.ValidationError("check out must be after the check in ")

        if overlapping_bookings.exists():
            raise serializers.ValidationError("This rooms is booked for this period.") 
        return attrs
    
    def create(self, validated_data):
        user_id = self.context.get("user")
        property_id = self.context.get("property_id")

        try:
            user_instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't exist")

        try:
            property_instance = models.Property.objects.get(id=property_id)
        except models.Property.DoesNotExist:
            raise serializers.ValidationError("Property does not exist")

        booked_nights = (validated_data['check_out_date'] - validated_data['check_in_date']).days
        validated_data['total_price'] = property_instance.price_per_night * booked_nights
        validated_data['property'] = property_instance
        validated_data['guest'] = user_instance
         
        
        booking=super().create(validated_data)
        return booking

class CreateConversationSerializer(serializers.ModelSerializer):
    participants=serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),many=True,required=False)

    class Meta:
        model=models.Conversation
        fields="__all__"
        read_only_fields=['participants']

    def create(self, validated_data):
        property_id=self.context['property_id']        
        try:
            property_instance=models.Property.objects.get(id=property_id)
        except models.Property.DoesNotExist:
            raise serializers.ValidationError("Property does not exist")

        host=property_instance.host.id
        request=self.context['request']
        client=request.user
        

        participants=validated_data.pop('participants',[])
        participants.append(client)
        if host not in participants:
            participants.append(host)


        conversation=super().create(validated_data)
        conversation.participants.set(participants)
        return conversation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = models.Message
        fields = ['id', 'sender', 'content', 'created_at']
        read_only_fields = ['sender']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    property = PropertySerializer(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    other_user = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Conversation
        fields = ['id', 'property', 'participants', 'messages', 'other_user', 'created_at', 'updated_at']
        read_only_fields = ['participants']

    def get_other_user(self, obj):
        request = self.context.get('request')
        if request and request.user:
            other_user = obj.participants.exclude(id=request.user.id).first()
            if other_user:
                return UserSerializer(other_user).data
        return None
