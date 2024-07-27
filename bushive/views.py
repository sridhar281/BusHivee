from django.shortcuts import render,redirect
from .models import *
from django.forms  import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .filters import busFilter,OrderFilter
from .forms import BuspaymentForm,ReservationForm
import razorpay
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token


def register(request): 
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,'Account was Created successfully for '+user )
                
            return redirect('login')
    context={'form':form}
    return render(request,'bus/registration.html',context)

def loginpage(request):
         if request.user.is_authenticated:
             return redirect('home')
         if request.method=='POST':
            username= request.POST.get('username')   
            password=request.POST.get('password')
        
            user=authenticate(request,username=username, password=password)
            if user is not None:
               login(request,user)
               return redirect('home')
            else:
              messages.info(request,"username or password is incorrect")  
         context = {}
         return render(request,'bus/login.html',context)


def logoutuser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request,'bus/home.html')

@login_required(login_url='login')
def trip_list(request):
    trips=Route.objects.all()
    triped=Trip.objects.all()
    myFilter=busFilter()
    context={'myFilter':myFilter,'trips':trips,'triped':triped}
    return render(request, 'bus/busbookings.html', context)


@login_required(login_url='login')
def queries(request):
    return render(request, 'bus/chatbot.html')


@login_required(login_url="login")
def track(request):
    user=User.objects.all()
    reservations=Reservation.objects.all()
    context={'reservations':reservations,'user':user}
    return render(request,'bus/track.html',context)

@login_required(login_url='login')
def about(request):
    buses=Trip.objects.all()
    total=buses.count()
    context={'buses':buses,'total':total}
    return render(request,'bus/about.html',context)

@login_required(login_url='login')
def payment(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        amount=int(request.POST.get('amount'))*100
        
        # create Razorpay client
        client = razorpay.Client(auth=('rzp_test_1wV97qLsLcZDQ7','PeJboZrLtCiAptveIOYeWNkn'))
        
        # CREATE ORDER
        response_payment=client.order.create(dict(amount=amount,currency='INR'))  
        print(response_payment)
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status=='created':
            #add data to database Buspayment
             bus_ticket = Buspayment(
                  name=name,
                  amount=amount,
                  order_id=order_id
                )
             bus_ticket.save()
             response_payment['name']=name
             
             form = BuspaymentForm(request.POST or None)
             context={'form':form,'payment':response_payment}
             return render(request,'bus/payment.html',context)
   
    form=BuspaymentForm()
    context={'form':form}
    return render(request,'bus/payment.html',context)


def payment_status(request):
    response=request.POST
    params_dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }
    #client instance
    client=razorpay.Client(auth=('rzp_test_1wV97qLsLcZDQ7','PeJboZrLtCiAptveIOYeWNkn'))
    try:
        status=client.utility.verify_payment_signature(params_dict)
        bus_ticket=Buspayment.objects.get(order_id=response['razorpay_order_id'])
        bus_ticket.payment_id=response['razorpay_payment_id']
        bus_ticket.paid=True
        bus_ticket.save()
        return render(request,'bus/payment_status.html',{'status':True})
    except:
        return render(request,'bus/paymentstatus.html',{'status':False})

# from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt 
# def payment_status(request):
#     if request.method == "POST":
#         payment_id = request.POST.get('razorpay_payment_id')
#         if payment_id: 
#             return redirect('bus/paymentstatus.html') 
#         else:
#             return redirect('payment-failure') 
#     return render(request, 'payment_status.html')


@login_required(login_url='login')
def sud(request):
    # Us=User.objects.get(id=pk_test)
    # context={'Us':Us}
    return render(request,'bus/singleuserdet.html')


@login_required(login_url='login')

def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservation_view')  
    else:
        form = ReservationForm()
    
    reservations = Reservation.objects.all()
    return render(request, 'reservation.html', {'form': form, 'reservations': reservations})