from django.shortcuts import redirect, render, get_object_or_404  # type: ignore
from django.views import generic  # type: ignore
from django.utils import timezone  # type: ignore
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import CartItem, Product

class IndexView(generic.ListView):
    """
    IndexView: Displays the latest products.
    """
    template_name = 'tanushdecors/index.html'
    context_object_name = 'latest_product_list'

    def get_queryset(self):
        """
        Fetches the latest 5 products published before or at the current time, ordered by publication date.
        """
        return Product.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

def product_list(request):
    products = Product.objects.all()
    return render(request, 'tanushdecors/products.html', {'products': products})

def shop(request):
    products = Product.objects.all()
    return render(request, 'tanushdecors/shop.html', {'products': products})

def about(request):
    return render(request, 'tanushdecors/about.html')

def services(request):
    return render(request, 'tanushdecors/services.html')

def blog(request):
    return render(request, 'tanushdecors/blog.html')

def contact(request):
    return render(request, 'tanushdecors/contact.html')

def thankyou(request):
    return render(request, 'tanushdecors/thankyou.html')

def login(request):
    return render(request, 'tanushdecors/login.html')

@login_required(login_url='login')  # Redirects to the login page if not logged in
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'tanushdecors/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required(login_url='login')  # Redirects to the login page if not logged in
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'tanushdecors/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required(login_url='login')  # Redirects to the login page if not logged in
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('tanushdecors:view_cart')

@login_required(login_url='login')  # Redirects to the login page if not logged in
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()

    return redirect('tanushdecors:view_cart')

@login_required(login_url='login')  # Redirects to the login page if not logged in
def order(request):
    if request.method == "POST":
        first_name = request.POST.get('c_fname')
        last_name = request.POST.get('c_lname')
        email = request.POST.get('c_email_address')
        phone = request.POST.get('c_phone')
        address = request.POST.get('c_address')
        state_country = request.POST.get('c_state_country')

        cart_items = CartItem.objects.filter(user=request.user)

        order_details = ""
        for item in cart_items:
            order_details += f"Product: {item.product.name}\n"
            order_details += f"Quantity: {item.quantity}\n"
            order_details += f"Price: ₹{item.product.price}\n\n"

        email_body = f"""
        Order Details:
        Name: {first_name} {last_name}
        Email: {email}
        Phone: {phone}
        Address: {address}, {state_country}

        Ordered Products:
        {order_details}
        Total Price: ₹{sum(item.product.price * item.quantity for item in cart_items)}
        """

        send_mail(
            subject="Order Confirmation",
            message=email_body,
            from_email="tanushdecor@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        cart_items.delete()

        return redirect('tanushdecors:order_success')

    return render(request, 'checkout.html')

def order_success(request):
    return render(request, 'tanushdecors/order_success.html')
