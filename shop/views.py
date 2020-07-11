from django.shortcuts import render, HttpResponse, redirect
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User # create user
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout #for login it authenticate
from django.contrib.auth.decorators import login_required # for login required




def index(request):
    allProds = []
    catprods = Product.objects.values( 'category','id')


    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)

        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
     
    params = {'allProds':allProds}

    
        
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    # return true ony  query matches the iteams 
    
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

    


def search(request):
    query  = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values( 'category','id')


    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query.lower(), item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if n != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
     
    params = {'allProds':allProds, 'msg':''}
    if len(allProds) == 0 or len(query) <4 :
        params = {'msg': 'plese make sure to enter revelent search query'}


    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank =False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank':thank})


 # function to track order details 

 # track orde details
def trackorder(orderId,mail):
    order = Orders.objects.filter(order_id=orderId, email=mail) 
    if len(order)>0:
        update = OrderUpdate.objects.filter(order_id=orderId)
        updates = []
        for item in update:
            updates.append({'text': item.update_desc, 'time': item.timestamp})
            response = {
            'status':'success',
                         'updates': updates,
                          'itemsJson':order[0].items_json, 
                          'totlePrice': order[0].amount,
                           'address':order[0].address,
                            'city':order[0].city,
                             'state':order[0].state,
                              'zip_code': order[0].zip_code, 
                              'phone': order[0].phone
                              }
                        
            return response                        
           
    else:
        return {"status":"noitem"}            
           


@login_required(login_url='signin')
def tracker(request):
    if request.method=="POST":
       
        orderId = request.POST.get('orderId', '')
        mail = request.POST.get('mail','')
                         
        try:
            
            response = json.dumps(trackorder(orderId,mail),default=str)
            return HttpResponse(response)

        except Exception as e:
            return HttpResponse('{"status":"error"}')
           
    return render(request, 'shop/tracker.html')





def productView(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})

@login_required(login_url='signin')
def checkout(request):
    if request.method=="POST":

        items_json = request.POST.get('itemsJson', '')    
        name = request.POST.get('name', '')
        amount = request.POST.get('amount','')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        test = {
                'cart':items_json,
                'name':name,
                'email':email,
                'address':address,
                'city':city,
                'state':state,
                'zip_code':zip_code,
                'phone':phone
            }
        for i in test:
            if (test[i] == '' or test[i] == '{}'):
                
                error = True
                return render(request, 'shop/checkout.html',{'empty':i, 'error':error})
            
        
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount, user =request.user)
        #, user_order = request.user.username
        print(order)
        # print(o)
       
        order.save()

        
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer amount to your account by user payment
        
    return render(request, 'shop/checkout.html')
@csrf_exempt
def handlerequest():
      #paytm will send you a post request
      pass
  

#Sign Up function
def signup(request):
    if request.method == 'POST':
        # Ger the post parameters
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #Checks for errorneous input
        if not (firstName+lastName).isalpha():
            messages.error(request,'name only contain letters')
            return redirect('signup')
        
        t = pass_verifi(pass1,pass2)
        if t[0] == False:
            messages.error(request,t[1])
            return redirect('signup')  

       

        #create the user
        myuser = User.objects.create_user(email, email, pass1)
        myuser.first_name = firstName
        myuser.last_name = lastName
        myuser.save()
        messages.success(request,'Your account has been created')
        return redirect('ShopHome')

    # else:
    #     return HttpResponse('error 404 - not allowed')
    return render(request,'shop/signup.html')
#Sign In function
def signin(request):
    if request.method == 'POST':
        loginEmail = request.POST['loginEmail']
        loginPassword = request.POST['loginPassword']

        user = authenticate(username=loginEmail, password = loginPassword)
        if user is not None:
            login(request, user)
            messages.success(request, 'successfully loged in')
            return redirect('ShopHome')
        else:
            messages.error(request, 'invailde credintial , plese try again !')
            return redirect('signin')
            
    return render(request,'shop/signin.html')    
@login_required(login_url='signin')
def signout(request):
   
        logout(request)
        messages.success(request, 'successfully loged out')
        return redirect('ShopHome')
    
#reset password   
def reset_password(request):
    if request.method == 'POST':
        resetEmail =  request.POST['resetEmail']
        new_pass1 = request.POST['newPass1']
        new_pass2 = request.POST['newPass2'] 
        try:
            

            user = User.objects.get(username=resetEmail)

            t = pass_verifi(new_pass1,new_pass2)
           
            if t[0] == False:
                messages.error(request,t[1])  
                return redirect ('reset-password')     

            user.set_password(new_pass1)
            user.save()
            messages.success(request, 'password is changed, Plese login with new credintial')
            return redirect('ShopHome')
        except Exception:
            messages.error(request,'user not exit')
            return redirect('reset-password')
           
    return render(request,'shop/reset-password.html')    

def pass_verifi(pass1,pass2):
    if len(pass1) <=6:
        return [False,'length of password must be greater then 6']
    elif pass1 != pass2:
        return [False, 'password is same as confirm password'] 
    else:
        return [True,'']       
        
def profile(request):
   
    return render(request,'shop/profile.html')

def orderList(request):
    myOrder = Orders.objects.filter(user=request.user)
    
   
    
    return render(request,'shop/orderlist.html',{'myOrder':myOrder})

    


