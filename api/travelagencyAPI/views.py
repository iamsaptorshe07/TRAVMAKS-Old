from django.shortcuts import render
from datetime import date
from travelagency.models import Tour, TourImage
from touring.models import Order,Cancelled_Order
from .serializers import TourSerializer, TourImageSerializer
from api.tours.serializers import OrderSerializer
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from travelagency.tests import *
from django.contrib.sites.shortcuts import get_current_site

class MyAgencyTour(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request):
        print("\nentered\n")
        if request.session.session_key:
            if request.session['access_type']=='seller':
                tour = Tour.objects.filter(seller=request.user)
                print("\n\n",tour,"\n\n")
                tourSerializer = TourSerializer(tour,many=True)
                for i in tourSerializer.data:
                    i['thumbnail']=str('http://')+str(get_current_site(request).domain)+str(i['thumbnail'])
                return Response(
                    {
                        'status':200,
                        'tours':tourSerializer.data,
                        'weblink':get_current_site(request).domain
                    }
                )
            else:
                return Response(
                    {
                        'status':404,
                        'message':'Not Authorized'
                    }
                )
        else:
            return Response(
                {
                    'status':404,
                    'message':'Not Authenticated'
                }
            )


        
class TourDetail(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request,tourId):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                try:
                    tour = Tour.objects.get(tourId=tourId,seller=request.user)
                    tourimages =TourImage.objects.get(tour=tour)
                except Exception as e:
                    print(e)
                    exception = {
                        'status':404,
                        'message':'Does Not Exist'
                    }
                    return Response(exception,status = status.HTTP_404_NOT_FOUND)
                data1 = TourSerializer(tour)
                data2 = TourImageSerializer(tourimages)
                description_data = data1.data['description'].split('@@@@')
                description = []
                for i in description_data:
                    lst = i.split('$$$$')
                    description.append(lst)
                day_title = []
                day_description = []
                for i in description:
                    day_title.append(i[0])
                    day_description.append(i[1])
                data1 = dict(data1.data)
                data1['description']={
                    'day_title':day_title,
                    'day_description':day_description
                }
                link = 'http://'+ str(get_current_site(request).domain)
                images = list(dict(data2.data.items()).values())
                mimg = []
                for i in range(1,len(images)-1):
                    if(images[i]!=None):
                        images[i]=link+str(images[i])
                        mimg.append(images[i])
                main_data = {
                    'tourdata':data1,
                    'tourimages':mimg,
                    'weblink':link
                }
                return Response(data = main_data,status=status.HTTP_200_OK)
            else:
                return Response(data={'message':'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={'message':'Not Authenticated'},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,tourId):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                try:
                    tour = Tour.objects.get(tourId=tourId,seller=request.user)
                    if tour.publish_mode:
                        maximum_people = request.POST.get('seat')
                        tour.maximum_people = maximum_people
                        tour.save()
                        return Response(
                            data={
                                'status':200,
                                'message':"successfully updated the seats"
                            },
                            status = status.HTTP_200_OK
                        )
                    else:
                        user = request.user
                        uid=user.id
                        agid=user.userAccess.agentId
                        sdate = request.POST.get('sdate')
                        edate = request.POST.get('edate')
                        print("\n\n",edate,"\n\n")
                        slocation = request.POST.get('slocation')
                        elocation = request.POST.get('elocation')
                        price = request.POST.get('price')
                        ttype = request.POST.get('ttype')
                        
                        special_tour_type=request.POST.get('additionalFeature')
                        print("\n\nspecial_tour_type--->>> ",special_tour_type,"\n\n")
                        specialOffer = request.POST.get('spoffer')
                        print("\n\nspecialOffer--->>> ",specialOffer,"\n\n")
                        if specialOffer:
                            specialOfferDescription = str(request.POST.get('spofferdetails')).strip()
                            print("\n\nspecialOfferDescription--->>> ",specialOfferDescription,"\n\n")
                        
                        ttitle = request.POST.get('ttitle')
                        inclusive = request.POST.get('inclusive')
                        exclusive = request.POST.get('exclusive')
                        highlight = request.POST.get('highlight')
                        overview = request.POST.get('overview')
                        maximum_people = request.POST.get('seat')
                        if tour.endDate != request.POST.get('edate'):
                            duration = tourDuration(request.POST.get('sdate'),request.POST.get('edate'))+1
                        else:
                            duration = tourDuration(request.POST.get('sdate'),request.POST.get('edate'))+1
                        
                        last_booking_date = request.POST.get('bookinglimit')
                        description_dct = ""
                        for i in range(duration):
                            description_dct=description_dct+str(request.POST.get('dayTitle{}'.format(i+1))).strip()+"$$$$"+str(request.POST.get('dayDescription{}'.format(i+1))).strip()+"@@@@"

                        #for i in range(duration):
                            #description_dct['dayTitle{}'.format(i+1)]=request.POST.get('dayTitle{}'.format(i+1)).strip()
                            #description_dct['dayDescription{}'.format(i+1)]=request.POST.get('dayDescription{}'.format(i+1)).strip()
                        print(description_dct)
                        slug = ''
                        for character in ttitle:
                            if character.isalnum():
                                slug+=character
                        slug+='_tourfrom_{}to{}_startingfrom{}_by{}-{}_tourId-{}_{}'.format(
                            slocation,elocation,sdate,agid,user.id,tourId,ttype
                        )
                        print('\n\n',slug,'\n\n')
                        description = description_dct.strip('@@@@')
                        tour.tourHeading = ttitle.strip()
                        tour.tourSlug = slug.strip()
                        tour.startingLocation = slocation.strip()
                        tour.endLocation = elocation.strip()
                        tour.endDate = edate.strip()
                        tour.description = description.strip()
                        tour.inclusive = inclusive.strip()
                        tour.exclusive = exclusive.strip()
                        tour.highlight = highlight.strip()
                        tour.price = price.strip()
                        tour.tour_type = ttype
                        if request.FILES.get('thumbnail') is not None:
                            tour.thumbnail = request.FILES.get('thumbnail')
                        tour.overview = overview.strip()
                        tour.maximum_people = maximum_people
                        tour.special_tour_type = special_tour_type
                        tour.specialOffer = specialOffer
                        if specialOffer:
                            tour.specialOfferDescription = specialOfferDescription
                        else:
                            tour.specialOfferDescription = None
                        tour.save()
                        image1 = request.FILES.get('image1')
                        image2 = request.FILES.get('image2')
                        image3 = request.FILES.get('image3')
                        image4 = request.FILES.get('image4')
                        image5 = request.FILES.get('image5')
                        image6 = request.FILES.get('image6')

                        tourImage = TourImage.objects.get(tour=tour)
                        if image1 is not None:
                            tourImage.image1 = image1
                        if image2 is not None:
                            tourImage.image2 = image2
                        if image3 is not None:
                            tourImage.image3 = image3
                        if image4 is not None:
                            tourImage.image4 = image4
                        if image5 is not None:
                            tourImage.image5 = image5
                        if image6 is not None:
                            tourImage.image6 = image6
                        tourImage.save()
                    
                        return Response(
                                data={
                                    'status':200,
                                    'message':"Successfully updated the tour!"
                                },
                                status = status.HTTP_200_OK
                            )   
                      
                except Exception as e:
                    print(e)
                    exception = {
                        'status':404,
                        'message':'Does Not Exist'
                    }
                    return Response(exception,status = status.HTTP_404_NOT_FOUND)
                    # Start writting your editting logic
            else:
                return Response(data={'message':'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={'message':'Not Authenticated'},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,tourId):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                try:
                    tour = Tour.objects.get(tourId=tourId,seller=request.user)
                except Exception as e:
                    print(e)
                    exception = {
                        'status':404,
                        'message':'Does Not Exist'
                    }
                    return Response(exception,status = status.HTTP_404_NOT_FOUND)
                
                if tour.publish_mode:
                    return Response(
                        data={
                            'status':401,
                            'message':'You are not authorized to delete the tour anymore'
                            },
                        status=status.HTTP_401_UNAUTHORIZED
                        )
                tour.delete()
                return Response(data={'message':'successfully deleted'},status=status.HTTP_200_OK)
            else:
                return Response(data={'message':'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={'message':'Not Authenticated'},status=status.HTTP_400_BAD_REQUEST)
                

class OngoingTour(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                ongoingTour = Order.objects.filter(agent=request.user,status=True,agent_approval=True)
                orders = []
                for i in ongoingTour:
                    if date.today() >= i.tour.startDate and date.today() <= i.tour.endDate:
                        orders.append(i)
                order_serializer = OrderSerializer(orders,many=True)
                return Response(
                    data = {
                        'status':200,
                        'ongoingTours':order_serializer.data
                    },
                    status = status.HTTP_200_OK
                )
            else:
                return Response(
                    data = {
                        'status':401,
                        'message':"Not Authorized"
                    },
                    status = status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                data = {
                    'status':404,
                    'message':"Not Authenticated"
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        
# Order Accept or Decline API
class AcceptOrDeclineTour(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def put(self,request,orderId):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                if Order.objects.filter(order_id = orderId,agent = request.user).exists():
                    order = Order.objects.get(order_id = orderId)
                    agent_approval = request.data
                    if agent_approval['approval']==True:
                        order.agent_approval = True
                        order.save()
                        return Response(
                            data = {
                                'status':200,
                                'message':"Congratualations! We are glad that you get booking through us"
                            },
                            status = status.HTTP_200_OK
                        )
                    elif agent_approval['approval'] == False:
                        cancelled_order = Cancelled_Order(
                            order_id = order.order_id,
                            tour = order.tour,
                            customer = order.customer,
                            customer_name = order.customer_name,
                            customer_email = order.customer_email,
                            customer_phone = order.customer_phone,
                            customer_address = order.customer_address,
                            agent = order.agent,
                            agency = order.agency,
                            total_people = order.total_people,
                            paid_by_user = order.paid_by_user,
                            total_price = order.total_price,
                            creation_date = order.creation_date,
                            cancelled_by = "AGENT",
                        )
                        cancelled_order.save()
                        tour = order.tour
                        tour.maximum_people+=order.total_people
                        tour.save()
                        order.delete()
                        return Response(
                            data = {
                                'status':200,
                                'mesaage':"Our Executives will call you please provide us a valid reason for not accepting the offer"
                            },
                            status = status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            data={
                                'status':406,
                                'message':"Send either true or false, only boolean value is allowed"
                            },
                            status = status.HTTP_406_NOT_ACCEPTABLE 
                            )
                else:
                    return Response(
                            data={
                                'status':404,
                                'message':"Order Not Found!"
                            },
                            status = status.HTTP_404_NOT_FOUND
                            )
            else:
                return Response(
                            data={
                                'status':401,
                                'message':"Not Authorized!"
                            }, 
                            status = status.HTTP_401_UNAUTHORIZED
                            )
        else:
            return Response(
                            data = {
                                'status':400,
                                'message':"Not Authenticated!"
                            },
                            status = status.HTTP_400_BAD_REQUEST
                            )

                    


class IncomingOrderStack(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                order = Order.objects.filter(agent=request.user,status=True,agent_approval=False)
                order_data = OrderSerializer(order,many=True)
                main_data = order_data.data
                for i in main_data:
                    tour = Tour.objects.get(id=int(i['tour']))
                    i['tourId'] = tour.tourId
                    i['tourName'] = tour.tourHeading
                    i['startLocation']=tour.startingLocation
                    i['endLocation']=tour.endLocation
                    i['startDate'] = tour.startDate
                    i['endDate']=tour.endDate
                    i['seatLeft']=tour.maximum_people
                    i['earning']=i['total_price']-i['paid_by_user']
                return Response(
                            data = {
                                'status':200,
                                'incoming_orders':main_data
                            },
                            status = status.HTTP_200_OK
                            )
            else:
                return Response(
                            data={
                                'status':401,
                                'message':"Not Authorized"
                            },
                            status = status.HTTP_401_UNAUTHORIZED
                            )
        else:
            return Response(
                data = {
                    'status':404,
                    'message':"Not Authenticated"
                },
                status = status.HTTP_400_BAD_REQUEST
            )


class OngoingUpcomingTour(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                order = Order.objects.filter(agent=request.user,status=True,agent_approval=True)
                upcomingOrders = []
                ongoingOrders = []
                for i in order:
                    if i.tour.startDate > date.today():
                        upcomingOrders.append(i)
                upcoming_order_serializer = OrderSerializer(upcomingOrders,many=True)
                for i in order:
                    if date.today() >= i.tour.startDate and date.today() <= i.tour.endDate:
                        ongoingOrders.append(i)
                ongoing_order_serializer = OrderSerializer(ongoingOrders,many=True)
                upcoming_data = upcoming_order_serializer.data
                ongoing_data = ongoing_order_serializer.data
                site = str(get_current_site(request))
                for i in ongoing_data:
                    tours = Tour.objects.get(id=i['tour'])
                    i['tour_name']=tours.tourHeading
                    i['amount_to_be_paid']=i['total_price']-i['paid_by_user']
                    i['tour_thumbnail']= site + tours.thumbnail.url
                    i['tour_slug']=tours.tourSlug
                    i['agent_name'] = tours.seller.name
                    i['agency_name']=tours.agency.agencyName
                    i['agency_id']=tours.agency.agency_Id
                    i['agent_id']=tours.seller.userAccess.agentId
                    i['agent_email']=tours.seller.email
                    i['agent_phone']=tours.seller.phNo
                    i['agency_email']=tours.agency.agencyEmail
                    i['agency_phone']=tours.agency.agencyPhNo
                    i['tour_id']=tours.tourId
                    i['tour_start_date']=tours.startDate
                    i['end_date']=tours.endDate
                    i['starting_location']=tours.startingLocation
                    i['ending_location']=tours.endLocation
                for i in upcoming_data:
                    tours = Tour.objects.get(id=i['tour'])
                    i['tour_name']=tours.tourHeading
                    i['amount_to_be_paid']=i['total_price']-i['paid_by_user']
                    i['tour_thumbnail']= site + tours.thumbnail.url
                    i['tour_slug']=tours.tourSlug
                    i['agent_name'] = tours.seller.name
                    i['agency_name']=tours.agency.agencyName
                    i['agency_id']=tours.agency.agency_Id
                    i['agent_id']=tours.seller.userAccess.agentId
                    i['agent_email']=tours.seller.email
                    i['agent_phone']=tours.seller.phNo
                    i['agency_email']=tours.agency.agencyEmail
                    i['agency_phone']=tours.agency.agencyPhNo
                    i['tour_id']=tours.tourId
                    i['tour_start_date']=tours.startDate
                    i['end_date']=tours.endDate
                    i['starting_location']=tours.startingLocation
                    i['ending_location']=tours.endLocation
                return Response(
                    data = {
                        'status':200,
                        'upcomingTours':upcoming_data,
                        'ongoingTours':ongoing_data
                    },
                    status = status.HTTP_200_OK
                )
            else:
                return Response(
                    data = {
                        'status':401,
                        'message':"Not Authorized"
                    },
                    status = status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                data = {
                    'status':404,
                    'message':"Not Authenticated"
                },
                status = status.HTTP_400_BAD_REQUEST
            )




class OrderBookingHistory(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                order_history = Order.objects.filter(agent=request.user,status=True,agent_approval=True)
                #cancel_history = Cancelled_Order.objects.filter(agent=request.user,status=True,agent_approval=True)
                #order_history = success_history.union(cancel_history).order_by('-creation_date')
                order_serializer = OrderSerializer(order_history,many=True)
                main_data = order_serializer.data
                for i in main_data:
                    tour = Tour.objects.get(id=int(i['tour']))
                    i['tourId'] = tour.tourId
                    i['tourName'] = tour.tourHeading
                    i['startLocation']=tour.startingLocation
                    i['endLocation']=tour.endLocation
                    i['startDate'] = tour.startDate
                    i['endDate']=tour.endDate
                    i['seatLeft']=tour.maximum_people
                    i['earning']=i['total_price']-i['paid_by_user']
                return Response(
                    data = {
                        'status':200,
                        'orderHistory':main_data
                    },
                    status = status.HTTP_200_OK
                )
            else:
                return Response(
                    data = {
                        'status':401,
                        'message':"Not Authorized"
                    },
                    status = status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                data = {
                    'status':404,
                    'message':"Not Authenticated"
                },
                status = status.HTTP_400_BAD_REQUEST
            )






class UpcomingTour(APIView):
    pass


class AddTour(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def post(self,request):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                user = request.user
                uid=user.id
                agid=user.userAccess.agentId
                sdate = request.POST.get('sdate')
                print("\n\n",sdate,"\n\n")
                edate = request.POST.get('edate')
                print("\n\n",edate,"\n\n")

                special_tour_type=request.POST.get('additionalFeature')
                print("\n\nadditionalFeature--->>> ",special_tour_type,"\n\n")
                specialOffer = request.POST.get('spoffer')
                print("\n\nspecialOffer--->>> ",specialOffer,"\n\n")
                if specialOffer:
                    specialOfferDescription = str(request.POST.get('spofferdetails')).strip()
                    print("\n\nspecialOfferDescription--->>> ",specialOfferDescription,"\n\n")

                slocation = request.POST.get('slocation')
                elocation = request.POST.get('elocation')
                price = request.POST.get('price')
                maximum_people = request.POST.get('seat')
                ttype = request.POST.get('ttype')
                thumbnail = request.FILES.get('thumbnail')
                ttitle = request.POST.get('ttitle')
                inclusive = request.POST.get('inclusive')
                exclusive = request.POST.get('exclusive')
                highlight = request.POST.get('highlight')
                overview = request.POST.get('overview')
                duration = tourDuration(request.POST.get('sdate'),request.POST.get('edate'))+1
                tourId = tourIdMaker()
                print('\n\n',tourId,'\n\n')
                description_dct = ""
                for i in range(duration):
                        description_dct=description_dct+str(request.POST.get('dayTitle{}'.format(i+1))).strip()+"$$$$"+str(request.POST.get('dayDescription{}'.format(i+1))).strip()+"@@@@"
                print(description_dct)
                slug = ''
                for character in ttitle:
                    if character.isalnum():
                        slug+=character
                slug+='_tourfrom_{}to{}_startingfrom{}_by{}-{}_tourId-{}_{}'.format(
                    slocation,elocation,sdate,agid,uid,tourId,ttype
                )
                print('\n\n',slug,'\n\n')
                description = description_dct.strip('@@@@')
                last_booking_date = request.POST.get('bookinglimit')
                
                
                tour = Tour(
                    #assign the values
                    seller = user,
                    agency = user.userAgency,
                    tourId = tourId,
                    tourSlug = slug.strip(),
                    tourHeading = ttitle.strip(),
                    startingLocation = slocation.strip(),
                    endLocation = elocation.strip(),
                    startDate = sdate,
                    endDate = edate,
                    description = description.strip(),
                    inclusive = inclusive.strip(),
                    exclusive = exclusive.strip(),
                    highlight = highlight.strip(),
                    price = price.strip(),
                    tour_type = ttype.strip(),
                    thumbnail = thumbnail,
                    overview = overview.strip(),
                    maximum_people = maximum_people.strip(),
                    last_booking_date = last_booking_date,
                    special_tour_type = special_tour_type,
                    specialOffer = specialOffer,
                    specialOfferDescription = specialOfferDescription,
                )
                tour.save()
                image1 = request.FILES.get('image1')
                image2 = request.FILES.get('image2')
                image3 = request.FILES.get('image3')
                image4 = request.FILES.get('image4')
                image5 = request.FILES.get('image5')
                image6 = request.FILES.get('image6')

                tourImage = TourImage(
                        tour = tour,
                        image1 = image1,
                        image2 = image2,
                        image3 = image3,
                        image4 = image4,
                        image5 = image5,
                        image6 = image6

                )

                tourImage.save()
                return Response(
                    data={
                        'status':200,
                        'message':"Sucessfully added tour!"
                    },
                    status = status.HTTP_200_OK
                )
            else:
                return Response(
                    data={
                        'status':404,
                        'message':"Not Authorized"
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                data = {
                    'status':404,
                    "message":"Not Authenticated"
                },
                status = status.HTTP_400_BAD_REQUEST
            )


