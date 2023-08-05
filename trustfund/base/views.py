from decimal import Decimal
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from celery import shared_task
from django.utils import timezone
from .management.commands.investment_completed import Command



from .serializers import *
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from django.db.models import Q
# Create your views here.

#user and jwt auth
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@shared_task
def increaseInterest():
    investments= Investment.objects.filter(completed=False)
    print(investments)
    for investment in investments:
       
        print(investment)
        #invst_interest=Decimal(investment.interest)
        invst_percentage = investment.percentage
        invst_duration =investment.duration
        invst_amount=investment.amount
        #invst_percentage_amount=invst_percentage/invst_duration
        total_interest =invst_percentage * invst_amount
        daily_interest=total_interest/invst_duration
        print(type(daily_interest))
        
        print(total_interest)
        investment.interest = investment.interest + daily_interest
        investment.user.profile.investment_wallet +=  daily_interest
        investment.user.profile.save()
        print(investment.interest)
        investment.save()
        if investment.interest >= total_interest:
            investment.completed=True
            investment.user.profile.investment_wallet = 0
            investment.user.profile.balance += total_interest
            investment.user.profile.save()
            investment.save()

#register user
@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'details': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)



#get useprofile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    #increaseInterest()
    #increaseVidCount()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserById(request,pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

#get users
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all().order_by('-date_joined')
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


#delete users
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')


# get profilemoredetails 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfileMoreDetails(request):

    user = request.user
    profiles = user.profile
    
    #print(profiles)
    
    serializer = ProfileSerializer(profiles, many=False)
   
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getProfiles(request):
    profiles = Profile.objects.all().order_by('-createdAt')

   
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserMoreProfileById(request,pk):
    
    profile = Profile.objects.get(_id=pk)
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProfile(request, pk):
    data = request.data
    profile =   Profile.objects.get(_id=pk)
    profile.name = data['name']
    profile.balance = Decimal(data['balance'])
    profile.investment_wallet = Decimal(data['investment_wallet'])
    profile.withdrawal_wallet = Decimal(data['withdrawal_wallet'])
    profile.country = data['country']
    profile.save()

    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)

# funding balance through payment api
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def fundWallet(request,pk):
    data = request.data
    profile = Profile.objects.get(_id=pk)
    profile.balance = profile.balance + Decimal(data['amount'])
    profile.save()
    serializer= ProfileSerializer(profile, many=False)
    return Response(serializer.data)

#debit balance when creating investment
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def DebitWallet(request,pk):
    data = request.data
    profile = Profile.objects.get(_id=pk)
    profile.balance = profile.balance - Decimal(data['invest_amount'])
    profile.save()
    serializer= ProfileSerializer(profile, many=False)
    return Response(serializer.data)

#funding investment wallet through main balance
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def fundInvestmentWallet(request,pk):
    data = request.data
    profile = Profile.objects.get(_id=pk)
    profile.investment_wallet = profile.investment_wallet + Decimal(data['amount'])
    profile.save()
    serializer= ProfileSerializer(profile, many=False)
    return Response(serializer.data)

#debiting investment wallet when Investment completed
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def DebitInvestmentWallet(request,pk):
    data = request.data
    profile = Profile.objects.get(_id=pk)
    profile.investment_wallet = profile.investment_wallet + Decimal(data['amount'])
    profile.save()
    serializer= ProfileSerializer(profile, many=False)
    return Response(serializer.data)

#fund withdrawal balance when user apply for withdrawal
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def fundWithdrawalBalance(request,pk):
    data = request.data
    profile = Profile.objects.get(_id=pk)
    profile.withdrawal_wallet = profile.withdrawal_wallet + Decimal(data['amount'])
    profile.save()
    serializer= ProfileSerializer(profile, many=False)
    return Response(serializer.data)

#user investment list
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserInvestments(request):
    user = request.user
    investment = user.investment_set.all().orderby_by('-createdAt')
    serializer = InvestmentSerializer(investment, many=True)
    return Response(serializer.data)


#create investment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creatInvestment(request):
    user = request.user
    data = request.data
    investment = Investment.objects.create(
        user = user,
        plan = data['plan'],
        amount = data['amount'],
    )
    serializer = InvestmentSerializer(investment, many=False)
    return Response(serializer.data)

#user withdrawal actions
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def applyForWithdrawal(request):
    data = request.data
    user = request.user
    
    withdrawal =withdrawal.objects.create(
        user = user,
        name = user.email,
        amount = data['amount'],
        accountName = data['accountName'],
        accountBank_Name =  data['accountBank_Name'],
        accountBank_Number = data['accountBank_Number'],
        payPalId = data['payPalId']
        )
    serializer = WithdrawalSerializer(withdrawal, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mywithdrawals(request):
    user = request.user
    withdrawals = user.withdrawal_set.all()
    serializer = WithdrawalSerializer(withdrawals, many=True)
    return Response(serializer.data)


def cronView(request):
    Command._private_function(request=request)




@api_view(['PUT'])   
def increaseVidCount(request):
    user = request.user.profile
    print(user)
    vidCount =user.vidCount
    print(vidCount)
    dailyLimit = user.dailyLimit
    watchAt=user.watchAt
    now = timezone.now()
    print(now)

    if (now - watchAt).total_seconds() >= 86400:
            user.vidCount = 0
            user.balance += 10
            user.save()
          
            print(user.vidCount)

    if vidCount < dailyLimit:
        user.vidCount += 1
        
        user.watchAt = now
        user.save()
        return Response({"msg":'video watch succesful'})
    else:
        return Response({"error": "You have reached the daily limit"})
   
        
            

  




    










