from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        starters = MenuItem.objects.filter(category__name__contains='Starter')
        maincourses = MenuItem.objects.filter(category__name__contains='MainCourse')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drinks')

        context = {
            'starters': starters,
            'maincourses': maincourses,
            'desserts': desserts,
            'drinks': drinks,
        }
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        # Get input fields at the bottom of the order template
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        town = request.POST.get('town')
        county = request.POST.get('county')
        post_code = request.POST.get('post')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=item)
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
            }
            order_items['items'].append(item_data)
        
        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
        
        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            town=town,
            county=county,
            post_code=post_code
        )
        order.items.add(*item_ids)

        # After everything is done, send confirmation email to user
        body = ('Thank you for your order!  Your food is being made and will be delivered soon!\n'
        f'Your total: {price}\n'
        'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'customer/order_confirmation.html', context)

class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items,
        }

        return render(request, 'customer/menu.html', context)

class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }
        return render(request, 'customer/menu.html', context)