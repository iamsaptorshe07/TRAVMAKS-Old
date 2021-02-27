from django.core.mail import send_mail 
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives 
from travmaks.settings import EMAIL_HOST_USER

def contactMessageSender(contact):
    mail_subject = "{} Agency has send a message".format(contact.name)
    toEmail = ['contact@travmaks.in']
    message = """ 
            Name = {}
            Email = {}
            Phone = {}
            Subject = {}
            message = {}
            """.format(contact.name,contact.email,contact.phone,contact.subject,contact.message)
    print(message)
    send_mail(
        mail_subject,
        message,
        from_email = EMAIL_HOST_USER, 
        recipient_list = toEmail,
        fail_silently=True

    )