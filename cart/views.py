from django.shortcuts import render, redirect
from .models import Cart, CartItem, Order, UserAddress
from beans.models import Coffee
from .forms import AddressForm, AddressSelectForm
from django.views.generic import View
from suds.client import Client
from cart.models import Order

def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    item_id = request.GET.get("item")
    qty = request.GET.get("qty", 1)
    if item_id:
        coffee = Coffee.objects.get(id=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=coffee)
        if int(qty) < 1:
            cart_item.delete()
        else:
            cart_item.quantity = int(qty)
            cart_item.save()
    return render(request, 'cart.html', {'cart': cart})

def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(cart=cart, user=request.user)

    if order.address == None:
        return redirect("cart:select_address")
    return redirect("") #Some payment page

def select_address(request):
    if UserAddress.objects.filter(user=request.user).count()<1:
        return redirect("cart:create_address")
    form = AddressSelectForm()
    form.fields['address'].queryset = UserAddress.objects.filter(user=request.user)
    if request.method == 'POST':
        form = AddressSelectForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            order = Order.objects.get(user=request.user)
            order.address=address
            order.save()
            return redirect("cart:checkout")
    context = {
        'form':form
    }
    return render(request, 'select_address.html', context)

def create_address(request):
    form = AddressForm()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address =form.save(commit=False)
            address.user = request.user
            address.save()
            form.save()
            return redirect("cart:select_address")
    context = {
        "form": form
    }
    return render(request, 'create_address.html', context)



def pay(request, order_id):
    order = Order.objects.get(id=order_id)
    payment_url = money(True, **{'customer': request.user,
                                'qty': '1',
                                'currency':'KWD',
                                'price': order.cart.total,
                                'order_id': order.id})
    return redirect(payment_url or 'payment:unsuccessful_payment')


def money(isTest, *args, **kwargs):
    if not isTest:
        client = Client('https://www.gotapnow.com/webservice/PayGatewayService.svc?wsdl')
    else:
        client = Client('http://live.gotapnow.com/webservice/PayGatewayService.svc?wsdl')

    payment_request = client.factory.create('ns0:PayRequestDC')

    customer = kwargs.get('customer')

    # Customer Info
    payment_request.CustomerDC.Email = customer.email
    payment_request.CustomerDC.Mobile = '60664602'
    payment_request.CustomerDC.Name = '%s %s'%(customer.first_name, customer.last_name)

    # Merchant Info
    if not isTest:
        payment_request.MerMastDC.MerchantID = tap_merchant_id
        payment_request.MerMastDC.UserName = tap_user
        payment_request.MerMastDC.Password = tap_password
        payment_request.MerMastDC.AutoReturn = 'Y'
        payment_request.MerMastDC.ErrorURL = 'http://127.0.0.1:8000/payment/unsuccessful_payment/'
        payment_request.MerMastDC.ReturnURL = 'http://127.0.0.1:8000/payment/successful_payment/'
    else:
        payment_request.MerMastDC.MerchantID = "1014"
        payment_request.MerMastDC.UserName = 'test'
        payment_request.MerMastDC.Password = "4l3S3T5gQvo%3d"
        payment_request.MerMastDC.AutoReturn = 'N'
        payment_request.MerMastDC.ErrorURL = 'http://127.0.0.1:8000/payment/unsuccessful_payment/'
        payment_request.MerMastDC.ReturnURL = 'http://127.0.0.1:8000/payment/successful_payment/'

    # Product Info
    mapping = {'CurrencyCode': kwargs.get('currency'), 'Quantity': kwargs.get('qty'),
               'UnitPrice': kwargs.get('price'),
               'TotalPrice': float(kwargs.get('qty')) * float(kwargs.get('price')),
               'UnitName': 'Order %s'%(kwargs.get('order_id'))}

    product_dc = {k: v for k, v in mapping.items()}
    payment_request.lstProductDC.ProductDC.append(product_dc)

    response = client.service.PaymentRequest(payment_request)
    paymentUrl = "%s?ref=%s"%(response.TapPayURL, response.ReferenceID)
    return paymentUrl

def successful_payment(request):
    ref_id = request.GET.get('ref', '')
    result = request.GET.get('result', '')
    pay_id = request.GET.get('payid', '')
    cardType = request.GET.get('crdtype', '')
    return redirect('cafe:coffee_list')

def unsuccessful_payment(request):
    return render(request, 'unsuccessful_payment.html', {})