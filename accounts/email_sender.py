from django.core.mail import send_mail 
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives 
from travmaks.settings import EMAIL_HOST_USER
def RequestCallBackMessageToAdmin(name,email,phone,agencyName,message):
    mail_subject = "{} Agency has requested a call back".format(agencyName)
    toEmail = ['travmaksagencysupport@travmaks.in']
    message = """ 
            Name = {}
            Email = {}
            Phone = {}
            Agency Name = {}
            message = {}
            """.format(name,email,phone,agencyName,message)
    print(message)
    send_mail(
        mail_subject,
        message,
        from_email = EMAIL_HOST_USER, 
        recipient_list = toEmail,
        fail_silently=True

    )