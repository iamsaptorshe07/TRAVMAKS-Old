from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.conf import settings

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "SECRET KEY = {}".format( reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="TRAVMAKS"),

        # message:
        email_plaintext_message,

        # from:
        settings.EMAIL_HOST_USER,

        # to:
        [reset_password_token.user.email], 
                
    )