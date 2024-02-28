from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Customer, Cart, OrderPlaced, ProductComment
from math import ceil
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import JsonResponse
from app.constants import MOBILE_CATEGORY, COMMENT_MESSAGE, REPLY_MESSAGE, USER_MESSAGE, USER_PROFILE_MESSAGE, VIVO, \
    SAMSUNG, BELOW, ABOVE


class ProductView(View):
    def get(self, request):
        allProds = []
        prod = Product.objects.values('category', 'id')
        cats = {item['category'] for item in prod}
        for cat in cats:
            prod = Product.objects.filter(category=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
            if allProds is not None:
                context = {'allProds': allProds}
            return render(request, 'app/index.html', context)
        return render(request, 'app/index.html')


class SearchProductView(View):
    def get(self, request):
        query_object = Q()
        query = request.GET.get('query')
        if query:
            query_object &= Q(title__icontains=query)
        product = Product.objects.filter(query_object)
        context = {'product': product}
        return render(request, 'app/search.html', context)


class ProductDetailView(View):
    def get(self, request, pk):

        product = Product.objects.get(pk=pk)
        comment = ProductComment.objects.filter(product=product, parent=None)
        replies = ProductComment.objects.filter(product=product).exclude(parent=None)
        reply_dict = {}
        for reply in replies:
            if reply.parent.id not in reply_dict.keys():
                reply_dict[reply.parent.id] = [reply]
            else:
                reply_dict[reply.parent.id].append(reply)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/product-detail.html',
                      {'product': product, 'item_in_cart': item_already_in_cart, 'comments': comment,
                       'reply_dict': reply_dict})

    def post(self, request):
        comment = request.POST.get("comment")
        user = request.user
        product_id = request.POST.get("product_id")
        product = Product.objects.get(id=product_id)
        reply_id = request.POST.get("reply_id")
        if reply_id == "":
            comment = ProductComment(comment=comment, user=user, product=product)
            comment.save()
            messages.success(request, COMMENT_MESSAGE)
        else:
            reply = ProductComment.objects.get(id=reply_id)
            comment = ProductComment(comment=comment, user=user, product=product, parent=reply)
            comment.save()
            messages.success(request, REPLY_MESSAGE)
        return redirect('product-detail', pk=product.pk)


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount
                totalamount = amount + shipping_amount
            return render(request, 'app/add-to-cart.html',
                          {'carts': cart, 'total_amount': totalamount, 'amount': amount})
        else:
            return render(request, 'app/empty-cart.html')


@login_required
def plus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount,
        }
        return JsonResponse(data)


@login_required
def minus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount,
        }
        return JsonResponse(data)


@login_required()
def remove_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        data = {
            'amount': amount,
            'total_amount': amount + shipping_amount,
        }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


@login_required
def orders(request):
    user = request.user
    order = OrderPlaced.objects.filter(user=user)
    return render(request, 'app/orders.html', {'order_placed': order})


class MobileDetailView(View):
    def get(self, request, data=None):
        query_object = Q()
        query_object &= Q(category__name=MOBILE_CATEGORY)
        if data == VIVO or data == SAMSUNG:
            query_object &= Q(category__name=MOBILE_CATEGORY, brand__brand_name=data)
        if data == BELOW:
            query_object &= Q(category__name=MOBILE_CATEGORY, discounted_price__lt=10000)
        if data == ABOVE:
            query_object &= Q(category__name=MOBILE_CATEGORY, discounted_price__gt=10000)
        mobiles = Product.objects.filter(query_object)
        return render(request, 'app/mobile.html', {'mobile': mobiles})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'users/customer-registration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, USER_MESSAGE)
            return redirect("customer-registration")
        return render(request, 'users/customer-registration.html', {'form': form})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        total_amount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add': add, 'total_amount': total_amount, 'cart_items': cart_items})


@login_required
def payment_done(request):
    user = request.user
    customer_id = request.GET.get("customer_id")
    customer = Customer.objects.get(id=customer_id)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):

    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            customer = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            customer.save()
            messages.success(request, USER_PROFILE_MESSAGE)
            return redirect("profile")
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
