from django.core.mail import send_mail 
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives 
from travmaks.settings import EMAIL_HOST_USER


def tourPublishedMailSender(tour):
    mail_subject = "{} is now published".format(tour.tourHeading)
    to_email = [tour.seller.email,tour.agency.agencyEmail]
    message = """ 
        Your tour {} is now published on TRAVMAKS. 
        Tour ID = {}
        You can't delete or edit the tour now. You can only update the tour sits.  
        For any assistance call us at +916290088603 / +918240568636.
    """.format(tour.tourHeading,tour.tourId)
    send_mail(
        mail_subject,
        message,
        from_email = EMAIL_HOST_USER, 
        recipient_list = to_email,
        fail_silently=True

    )



def newTourAddedToAdminMail(tour):
    subject = "{} agency has added a new tour".format(tour.agency.agencyName)
    to_email = ['travmaksagencysupport@travmaks.in']
    message = """
        {} has added a new tour.
        Tour Name = {}
        Tour Start Date = {}
        Tour End Date = {}
        Tour Start Location = {}
        Tour End Location = {}
        """.format(
            tour.agency.agencyName,
            tour.tourHeading,
            tour.startDate,
            tour.endDate,
            tour.startingLocation,
            tour.endLocation
            )
    send_mail(
    subject,
    message,
    from_email = EMAIL_HOST_USER, 
    recipient_list = to_email,
    fail_silently=True)
