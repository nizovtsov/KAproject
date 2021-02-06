from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm


from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart
# Create your views here.


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    #products = cart_obj.products.all()
    #print(products)
    #total = 0
    #for x in products:
    #    print(x.title)
    #    total += x.price
    #print(total)
    #cart_obj.total = total
    #cart_obj.save()
    #cart_id = request.session.get("cart_id", None)
    #qs = Cart.objects.filter(id=cart_id)
    #if qs.count() == 1:
    #    print('Cart ID exists')
    #    cart_obj = qs.first()
    #    if request.user.is_authenticated() and cart_obj.user is None:
    #        cart_obj.user = request.user
    #        cart_obj.save()
    #else:
    #    cart_obj = Cart.objects.new(user=request.user)
    #    request.session['cart_id'] = cart_obj.id
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    #print(request.POST)
    product_id = request.POST.get("product_id")
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("show message to user? product is gone")     #TODO
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)  # cart_obj.products.add(product_id)

        request.session['cart_items'] = cart_obj.products.count()
    #return redirect(product_obj.get_absolute_url())
    return redirect("cart:home")



def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    #user = request.user
    #billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_form = AddressForm()

    billing_profile, billing_profile_created = BillingProfile.object.new_or_get(request)
    #guest_email_id = request.session.get('guest_email_id')

    #if user.is_authenticated():
    #    'logged in user checkout; remember payment stuff'
    #    billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    #elif guest_email_id is not None:
    #    'guest user checkout; auto reloads payment stuff'
    #    guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
    #    billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    #else:
    #    pass

    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj) #in Orders OrderManager
        ##order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        ##if order_qs.count() == 1:
        ##    order_obj = order_qs.first()
        ##else:
            #old_order_obj = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
            #if old_order_obj.exists():
            #    old_order_obj.update(active=False)
        ##    order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)
#        order_qs = Order.objects.filter(cart=cart_obj, active=True)
#        if order_qs.exists():
#            order_qs.update(active=False)
#        else:
#            order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "billing_address_form": billing_address_form,
    }
    return render(request, "carts/checkout.html", context)
