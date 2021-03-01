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
def agencySignupMailSenderToAdmin(agency):
    subject = "{} has signed up".format(agency.agencyName)
    mail_to = ["travmaksagencysupport@travmaks.in"]
    message = """
            {} has signed up!
            ------------------------------------------
            Agency Name : {}
            Agency Email :{}
            Agency Contact No: {}
            ------------------------------------------
            Agent Name : {}
            Agent Email : {}
            Agent Contact No : {}
            ------------------------------------------
              """.format(
                  agency.agencyName,
                  agency.agencyName,
                  agency.agencyEmail,
                  agency.agencyPhNo,
                  agency.user.name,
                  agency.user.email,
                  agency.user.phNo,
              )
    send_mail(
        subject,
        message,
        from_email = EMAIL_HOST_USER, 
        recipient_list = mail_to,
        fail_silently=True)

def sellerAccountApproovedMail(agencyName,agencyId,agentId,destinationEmail):
    mail_subject = "{} is now verified and a TRAVMAKS partner".format(agencyName)
    toEmail = destinationEmail
    message = """ 
            Your agency {} is now verified and you can start adding tours. For any query you 
            can call +91 6290088603 / +91 8240568636. Or you can mail agencysupport@travmaks.in .
            Your agency name = {}
            Your unique agency-Id = {}
            Your unique agent-Id = {}
            """.format(agencyName,agencyName,agencyId,agentId)
    print(message)
    send_mail(
        mail_subject,
        message,
        from_email = EMAIL_HOST_USER, 
        recipient_list = toEmail,
        fail_silently=True

    )
    