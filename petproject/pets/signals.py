from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Delivery_details
from django.core.mail import send_mail
from pets.models import pets 


@receiver(post_save, sender=Delivery_details)
def handle_successful_delivery(sender, instance, **kwargs):
    print('asdfbhjkl')
    if instance.delivery_status=='delivered':
        cart_item = instance.pet 
        pet = cart_item.pet  

        pet.quantity -= 1
        pet.save()

        user_email = '2017btt012@sggs.ac.in' #instance.user.email  
        send_mail(
            subject='Your Pet Delivery Confirmation',
            message=f'Dear {instance.user.name},\n\n'
                    f'Thank you for your purchase!\n'
                    f'Here are your delivery details:\n\n'
                    f'Pet: {pet.name} ({pet.breed}, {pet.gender}, Age: {pet.age})\n'
                    f'Delivery Token: {instance.user_token}\n'
                    f'Amount Paid: {instance.amount}\n'
                    f'Delivery Address: {instance.address}\n\n'
                    f'We hope your pet reaches you safely!\n\n'
                    f'Best regards,\nThe Pet Store Team',
            from_email='dakreshashank@gmail.com',  
            recipient_list=[user_email],  
            fail_silently=False,
        )