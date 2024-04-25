from django.shortcuts import render
from . models import Category,Product
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from . models import UserCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Wishlist,Brand
from django.http import HttpResponse
from .models import Contact_us,Order
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
 
# client=razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID,settings.KEY_SECRET))
  
def base(request): 
    return render(request,'base.html')
def index(request):
    products=Product.objects.filter(section__name='DEALS OF THE DAY')
    recomended=Product.objects.filter(section__name='RECOMENDED FOR YOU')
    ney=Product.objects.get(slug='puma-mens-future-ultimate-fgag-persian-greenwhite')
        
    context={
        'products':products,
        'recomended':recomended,
        'ney':ney
    }
    return render(request,'index.html',context)
def product(request):
    category=Category.objects.all()
    brand=Brand.objects.all()
    category_id=request.GET.get('category')
    brand_id=request.GET.get('brand')
    if category_id:
        products=Product.objects.filter(subcategory = category_id)
    elif brand_id:
        products=Product.objects.filter(brand=brand_id)
    else:
       products=Product.objects.all()
           
    context={
        'category':category,
        'products':products,
        'brand':brand,
    }    
    return render(request,'products.html',context)

#Define a view function for user signup
def signup(request):
    # Check if the request method is POST
    #login
    if request.method == 'POST':
        # Initialize the UserCreateForm with POST data
        form = UserCreateForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            # Save the user and get the new_user instance
            new_user = form.save()
            
            # Authenticate the user using the entered username and password
            authenticated_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            
            # Log in the authenticated user
            if authenticated_user is not None:
              login(request, authenticated_user)
                # Redirect to the 'index' page
              return redirect('login')
            else:
               messages.error(request,'inavalid username or password')
            

    # If the request method is not POST (i.e., it's a GET request), initialize a new form
    #signup page
    else:
        form = UserCreateForm()

    # Create a context dictionary with the form
    context = {
        'form': form
    }

    # Render the 'signup.html' template with the context
    return render(request,'registration/signup.html', context)


#cart

@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart=Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product)
    return redirect("index")


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_increment(request,id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    
    # Check if the product exists in the cart before attempting to decrement
    if str(product.id) in cart.cart:
        if cart.cart[str(product.id)]['quantity'] > 1:
            cart.decrement(product=product)
        else:
            cart.remove(product=product)
    
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")




@login_required(login_url="/accounts/login")
def cart_detail(request):
    cart_items = request.session.get('cart', {})  # Fetch cart items from session
    product_details = []  # List to hold calculated product details

    for cart_item in cart_items.keys():
        product = Product.objects.get(id=int(cart_item))
        quantity = cart_items[cart_item]['quantity']
        discounted_price = product.price - (product.price * product.discount / 100)
        subtotal = discounted_price * quantity
        # payment = client.order.create({
        #     'amount': 500 * 100,  # Amount should be in paisa
        #     'currency': 'INR',
        #     'payment_capture': 1  # Auto-capture payment when successful (1 for true)
        #  })
        # # print(payment)
        # order_id=payment['id']
        
        product_detail = {
            'product': product,
            'quantity': quantity,
            'discounted_price': discounted_price,
            'subtotal': subtotal,
            
        }
        product_details.append(product_detail)
    
    total = sum(item['subtotal'] for item in product_details)
    if (sum(item['subtotal'] for item in product_details) >2999):
        lastprice=total
    else:
        lastprice=total+120

    context = {
        'product_details': product_details,
        'total': total,
        'lastprice':lastprice
        # 'payment':payment,
        # 'order_id':order_id
    }
    return render(request, 'cart/cart_detail.html', context)


#wishlist

@login_required(login_url="/accounts/login")
def add_to_wishlist(request, id):
    product = Product.objects.get(id=id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect("index")

@login_required(login_url="/accounts/login")
def remove_from_wishlist(request, id):
    product = Product.objects.get(id=id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    return redirect("wishlist_detail")

@login_required(login_url="/accounts/login")
def wishlist_detail(request):
   
      wishlist = Wishlist.objects.get(user=request.user)
      products = wishlist.products.all()
      for p in products:
        p.discounted_price=p.price - (p.price * p.discount / 100)
    
      context = {
        'products': products,
      }
      return render(request, 'wishlist/wishlist_detail.html', context)
    

def contact_page(request):
    if request.method=="POST":
        contact=Contact_us(
             name=request.POST.get('name'),
             email=request.POST.get('email'),
             subject=request.POST.get('subject'),
             message=request.POST.get('message'),
        )
        contact.save()
    
    return render(request,'contact.html')

def checkout(request):
    if request.method =="POST":
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        pincode=request.POST.get('pincode')
        cart=request.session.get('cart')
        uid=request.session.get('_auth_user_id')
        user=User.objects.get(pk=uid)
        order_id=request.POST.get('order_id')
        payment=request.POST.get('payment')
        lastprice = request.POST.get('lastprice')
        print(order_id,payment,user)
        context={
            
          'order_id':order_id,
          'payment':payment,
        }
        for product_id, item in cart.items():
            product = Product.objects.get(pk=product_id)
            quantity = item['quantity']
            price = float(item['price'])
            total = price * quantity
            discounted_price = price - (price * product.discount / 100)
        
        for i in cart:
            a=(float(cart[i]['price']))
            b=cart[i]['quantity']
            total=a*b
            
            order=Order(
                user=user,
                product=cart[i]['name'],
                price=cart[i]['price'],
                quantity=cart[i]['quantity'],
                image=cart[i]['image'],
                address=address,
                phone=phone,
                pincode=pincode,
                payment_id=payment,
                total=total,
                lastprice=lastprice,
                discounted_price=discounted_price,
            )
            order.save()
        request.session['cart']={}
        
        return render(request,'cart/thankyou.html',context)
        # return render(request,'cart/cart_detail.html',context)
        
    return HttpResponse('checkoutpage')



def ur_order(request):
    uid=request.session.get('_auth_user_id')
    user=User.objects.get(pk=uid)
    order=Order.objects.filter(user=user)
    for o in order:
         o.discounted_price = float(o.discounted_price)
         o.quantity = int(o.quantity)
         o.final_price = o.discounted_price * o.quantity
    context={
        'order':order
    }
    return render(request,'order.html',context)

def delete_order_item(request, order_item_id):
    order_item = get_object_or_404(Order, pk=order_item_id)
    order_item.delete()
    return redirect('order') 

#single product view

def product_details(request,slug):
    # product=Product.objects.get(slug=slug)
    # if product.exist():
    #     product=Product.objects.get(slug=slug)
    # else:
    #     return redirect('404')
    product = get_object_or_404(Product, slug=slug)
    r_products = Product.objects.filter(subcategory=product.subcategory).exclude(slug=slug)[:4]
    context={
        'product':product,
        'r_products':r_products
    }
    return render(request,'product/product_detail.html',context)

def about(request):
    return render(request,'about_us.html')
@csrf_exempt
def success(request):
    if request.method=="POST":
        a=request.POST
        # print(a)
        order_id="razorpay_order_id"
        for key,val in a.items():
           if key == 'razorpay_order_id':
               order_id=val
               break
        user=Order.objects.filter(payment_id=order_id).first() 
        # print(user)
        if user:
           user.paid= True
           user.save()
    return render(request,'cart/thankyou.html')
# @csrf_exempt
# def success(request):
#     if request.method == "POST":
#         razorpay_order_id = request.POST.get('razorpay_order_id')
#         if razorpay_order_id:
#             user = Order.objects.filter(payment_id=razorpay_order_id).first()
#             # print(user)
#             if user:
#                 user.paid = True
#                 user.save()
#     return render(request, 'cart/thankyou.html')




# def error404(request,exception):
#    return render(request,'errors/404.html',status=404)