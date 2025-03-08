from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now 
from datetime import timedelta
from booking.models import WaitListEntry
from django.core.mail import send_mail


def process_next_waitlist_entry(property_id,user_id):
    User=get_user_model()
    user=User.objects.get(user=user_id)
    next_entry = WaitListEntry.objects.filter(
            related_property=property_id,
            confirmed=False,
            notified_at=None
    ).first()
    
    if next_entry:
        next_entry.notified_at =now()
        wait_time =next_entry.notified_at
        next_entry.save()

    subject="Reservation waitlist"
    message =f" A property on your wishlist is available please confirm reservation before {wait_time} or we or we will be cancel your waitlist reservation"

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list =[user.email]

    send_mail(subject,message,from_email,recipient_list)
    print("Email sent .")
