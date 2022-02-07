from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import auth,messages
from cart.models import Cart,CartItems
from .models import order,order_list,order_note_admin,invoice
from bookstore.models import Book

def checkout_req(request):
    if request.POST:
        req_user = request.user

        if req_user.is_authenticated:
            # working on order model
            client = request.user
            order_note = request.POST['order_note']

            # Unsafe to grab total from get or post req
            # So, I think it's bettter for me to comment out this line.
            # But I could have used it because it's a university project
            # and not many people is going to use it in their production environment. Feel free to use if if you like

            # total = request.POST['total']


            order_save = order.objects.create(
                client=client,
               # order_note_user=order_note,

            )
            order_save.save()

            # working on order_list


            session = request.session.session_key
            cart = Cart.objects.get(cart_session=session)
            cart_items_list = CartItems.objects.all().filter(cart=cart)
            total = 0

            for item in cart_items_list:

                order_item= Book.objects.get(title=item.book)
                price = order_item.price
                quantity = item.quantity
                total += price*quantity

                order_list_save = order_list.objects.create(
                    order_id=order_save,
                    order_item=order_item,
                    order_price=price,
                    order_quantity=quantity
                )
                order_list_save.save()

            # working on invoice

            total_price = total
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            city = request.POST['city']
            division = request.POST['division']
            zip = request.POST['zip']
            country = request.POST['country']



            save_invoice = invoice.objects.create(
                total_price=total_price,
                first_name=first_name,
                address=address,
                last_name=last_name,
                division=division,
                city=city,
                zip=zip,
                country=country,
            )
            save_invoice.save()

        else:
            return redirect("login")
    else:
        return redirect("register")


def checkout_page(request):
    if request.user.is_authenticated:
        return render(request, "checkout.html")
    else:
        messages.error(request,"You need to be registered to place an order ")
        return redirect("register")

