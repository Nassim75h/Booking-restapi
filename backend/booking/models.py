from authapp.models import User
from django.conf import settings 
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from BookingApplication.constants import PROPERTY_STATUS_CHOICES
import uuid
from django.core.exceptions import ValidationError


class Property(models.Model):
    
    title=models.CharField(max_length=50)
    address=models.CharField(max_length=255)
    # TODO add cities package and make this into choice field
    city=models.CharField(max_length=100)
    max_guests=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # TODO we can change this to be custom table
    price_per_night=models.DecimalField(max_digits=10,decimal_places=2)
    # TODO add corrdinates
    host=models.ForeignKey(User,related_name='host',on_delete=models.CASCADE)
    description=models.TextField(blank=True,null=True)
    category=models.CharField(max_length=50,blank=True)
    available_from=models.DateTimeField(blank=True,null=True)
    available_to=models.DateTimeField(blank=True,null=True)
    blocked_dates=models.JSONField(default=list,blank=True,null=True)
    is_available=models.BooleanField(default=True)

    class Meta:
        verbose_name = ("Property")
        verbose_name_plural =("Properties")

    def __str__(self) -> str:
        return self.title
    
class PropertyImage(models.Model):
    image=models.ImageField(upload_to='property_images',null=True,blank=True)
    related_property=models.ForeignKey('Property',on_delete=models.CASCADE,related_name="images")

class Amenity(models.Model):
    #TODO add more attributes
    name=models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name
    class Meta:
        verbose_name_plural="Amenities"
  
  
        
class PropertyAmenity(models.Model):

    # TODO: remove the null blank
    related_property=models.ForeignKey("Property",on_delete=models.CASCADE)
    amenities=models.ForeignKey("Amenity",on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural='PropertyAmenities'
        

class Booking(models.Model):
    guest=models.ForeignKey(User,on_delete=models.CASCADE)
    property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name='property')
    check_in_date=models.DateField()
    check_out_date=models.DateField()
    # TODO create function to calculate the price depending on time or residance
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(choices=PROPERTY_STATUS_CHOICES.choices,
                            default=PROPERTY_STATUS_CHOICES.PENDING,
                            max_length=10
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_paid=models.BooleanField(default=False)
    stripe_session_id=models.CharField(max_length=255,blank=True,null=True)
    def __str__(self):
        return f"Booking {self.id} - {self.property.title}"

class Review(models.Model):
    booking=models.ForeignKey("Booking",on_delete=models.CASCADE)
    guest=models.ForeignKey(User,on_delete=models.CASCADE)
    # TODO: remove the null and blank from propert_related
    related_property=models.ForeignKey("Property",on_delete=models.CASCADE,null=True,blank=True)
    rating=models.IntegerField(
            blank=True,
            null=True,
            validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
    ])
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    
class WaitListEntry(models.Model):
    guest=models.ForeignKey(User,on_delete=models.CASCADE)
    related_property=models.ForeignKey("Property",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    notified_at = models.DateTimeField(blank=True,null=True)
    confirmed = models.BooleanField(default=False)

    class Meta :
        ordering= ['created_at']
        verbose_name_plural="WaitList Entries"
    
    def __str__(self):
        return f" user:{self.guest} confirmed :{self.confirmed}"
        
class Conversation(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    participants=models.ManyToManyField(User)
    created_at=models.DateTimeField(auto_now_add=True)

    def participant_names(self):
        return ", ".join([user.username for user in self.participants.all()])
    
    participant_names.short_description="Participants"

    def __str__(self):
        names=", ".join([user.username for user in self.participants.all()])
        return f"{names}"


class Message(models.Model):
    conversation=models.ForeignKey(Conversation,on_delete=models.CASCADE)
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    time_stamp=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)
    
    def clean(self):
        if self.sender not in self.conversation.participants.all():
            raise ValidationError("Sender must be a participant in the conversation.")
    
    


