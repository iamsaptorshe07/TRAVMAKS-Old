from django.core.mail import send_mail 
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives 
from travmaks.settings import EMAIL_HOST_USER


def orderRecieveMailSender(order):
    mail_subject = "Booking order from TRAVMAKS"
    to_email = [order.agent.email,order.agency.agencyEmail]
    message = """ 
        You have got an order for the tour {}. 
        Order-Id = {}
        Tour-Id = {}
        Your Earning = {}
        To accept the offer please go to the incoming order section 
        of you dashboard and accept the offer.   
        For any assistance call us at +916290088603 / +918240568636.
    """.format(order.tour.tourHeading,order.order_id,order.tour.tourId,order.total_price - order.paid_by_user)
    send_mail(
        mail_subject,
        message,
        from_email = EMAIL_HOST_USER, 
        recipient_list = to_email,
        fail_silently=True

    )


def orderAcceptMailSender(order):
    mail_subject_agency = "Congratulations! On your order"
    to_agency = [order.agent.email,order.agency.agencyEmail]
    messageToAgency = """ 
        You have confirmed the tour package {} booking order. 
        Order-Id = {}
        Tour-Id = {}
        Customer Email = {}
        Customer Name = {}
        Customer Contact No = {}
        Total Budget customer will pay you = {}
        Total No of people going on the tour = {}   
        For any assistance call us at +916290088603 / +918240568636.
    """.format(order.tour.tourHeading,
    order.order_id,
    order.tour.tourId,order.customer_email,order.customer_name,order.customer_phone,
    order.total_price - order.paid_by_user,order.total_people)
    send_mail(
        mail_subject_agency,
        messageToAgency,
        from_email = EMAIL_HOST_USER, 
        recipient_list = to_agency,
        fail_silently=True

    )
    subject_user = "Your booking {} is confirmed".format(order.tour.tourHeading)
    to_user = [order.customer_email,order.customer.email]
    messageToUser = """
    Your booking is confirmed from agency, we have shared the details of the agency 
    with this mail. You can contact the person whose details have been shared from our end.
    Tour name = {}
    Tour Id = {}
    Order Id = {}
    Agency Name = {}
    Agency Email = {}
    Agency Phone = {}
    Agency Id = {}
    Agent Id = {}
    Agent Name = {}
    Agent Email = {}
    Agent Phone = {}  
    Amount paid by you = {}
    Amount to be paid by you to agency = {}
    Thank You
    """.format(order.tour.tourHeading,
    order.tour.tourId,
    order.order_id,
    order.agency.agencyName,
    order.agency.agencyEmail,
    order.agency.agencyPhNo,
    order.agency.agency_Id,
    order.agent.userAccess.agentId,
    order.agent.name,
    order.agent.email,
    order.agency.agencyPhNo,
    order.paid_by_user,
    order.total_price - order.paid_by_user
    )
    send_mail(
        subject_user,
        messageToUser,
        from_email = EMAIL_HOST_USER, 
        recipient_list = to_user,
        fail_silently=True

    )
    




def orderMailToAdmin(order,subject):
    mail_subject = subject
    reciever = ['booking@travmaks.in']
    message = """
     --------------------------------Tour Information -------------------------------- 
        Tour Name : {}
        Tour Id : {}
        Tour Starting Location : {}
        Tour Ending Location : {}
        Tour Starting Date : {}
        Tour Ending Date : {}
    -------------------------------- Agent Information ----------------------------------
        Agent Name : {}
        Agent Id : {}
        Agent Email : {}
        Agent Phone : {}
    --------------------------------- Agency Information ------------------------------
        Agency Name : {}
        Agency ID : {}
        Agency Email : {}
        Agency Contact No : {}
    -------------------------------- Customer Information ---------------------------------
        Customer Name : {}
        Customer Email : {}
        Customer Phone : {}
    --------------------------------- Price Information ------------------------------------
        Total No of people going : {}
        Total Cost :{}
        Paid to TRAVAKS : {}
        To be paid to {} : {}
    """.format(
        order.tour.tourHeading,
        order.tour.tourId,
        order.tour.startingLocation,
        order.tour.endLocation,
        order.tour.startDate,
        order.tour.endDate,

        order.agent.name,
        order.agent.userAccess.agentId,
        order.agent.email,
        order.agent.phNo,

        order.agency.agencyName,
        order.agency.agency_Id,
        order.agency.agencyEmail,
        order.agency.agencyPhNo,

        order.customer_name,
        order.customer_email,
        order.customer_phone,

        order.total_people,
        order.total_price,
        order.paid_by_user,
        order.agency.agencyName,
        order.total_price - order.paid_by_user
    )
    send_mail(
         mail_subject,
        message,
        from_email = EMAIL_HOST_USER, 
        recipient_list = reciever,
        fail_silently=True

    )
