from django.forms.formsets import  formset_factory
from django.shortcuts import redirect, render
from .models import Department, Item, Sale, Cart
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ItemFormCRUD, SaleForm, NewSaleForm, SearchSaleForm, UpdateCartForm
from django.contrib import messages
from django.db.models import Q
from datetime import  datetime, timedelta 
from django.forms import modelformset_factory, formset_factory


# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    items = Item.objects.filter(Q(department__name__icontains=q))   
    items = items[:7]
    item_count = items.count()
    departments = Department.objects.all()
    context = {'departments': departments, "items": items, "item_count": item_count}
    return render(request, 'app/home.html', context)


def department(request, pk):
    department = Department.objects.get(id=pk)
    print(department)
    items = Item.objects.filter(department=department)
    items=items[::-1]
    return render(request, 'app/department.html', {"department": department, "items": items})


def all_items(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    filtered_items = Item.objects.filter(Q(name__icontains=q))
    items = Item.objects.all()
    context = {"items": items, "filtered_items": filtered_items, "zero": 0}
    return render(request, 'app/view_items.html', context)

def item(request, pk):
    item = Item.objects.get(id=pk)
    context = {"item": item,}
    return render(request, 'app/item.html', context)


def add_item(request, pk):
    department = Department.objects.get(id=pk)
    form = ItemFormCRUD()
    items = Item.objects.filter(department=department)
    if request.method == 'POST':
        form = ItemFormCRUD(request.POST)

        if form.is_valid():
            if department:
                item = form.save(commit=False)
                item.department = department
                item.save()
                items = items[::-1]
                return render(request,'app/department.html', {"department": department, "items": items})
               
    context_dict = {"form": form, "department": department}
    return render(request, 'app/add_item.html', context_dict)
 

def update_item(request, pk):  
    item = Item.objects.get(id=pk)
    item_quantity = item.quantity
    form = ItemFormCRUD(instance=item)
    if request.method == 'POST':
        form = ItemFormCRUD(request.POST, instance=item)

        if form.is_valid():
            item_instance = form.save(commit=False)
            item_instance.updated = datetime.now()
            print(item_instance.updated)
            if not item_instance.quantity < item_quantity:
                item_instance.save()
                messages.success(request, "Successfully updated item")
            else:
                return HttpResponse("You are not allowed to reduce item's quantity")
            return render(request, 'app/item.html', {"item": item_instance})
        else:
            print(form.errors)

    context_dict = {"form": form, "department": department}
    return render(request, 'app/update_item.html', context_dict)


def delete_item(request, pk):
    form = ItemFormCRUD()
    item = Item.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('home')

    context_dict = {"form": form, "item": item}
    return render(request, 'app/delete.html', context_dict)



def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    page = "login_page"
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try: 
            user = User.objects.get(username=username)
        except:
            return HttpResponse("User does not Exist")

        user = authenticate(request, username=username, password=password)
        
        if not user:
            return HttpResponse("Invalid credentials")
        login(request, user)
        return redirect('home')
    elif request== "GET":
        return login_user(request)
    
    context = {"page": page}
    return render(request, 'app/register_login.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')
    

def update_quantity(x, y):
    item = Item.objects.get(id=y)
    sale = Sale.objects.get(id=x)
    item.quantity = item.quantity - sale.quantity
    item.price = item.price
    item.save()
    


def view_sales(request):
    if request.user.is_superuser or request.user.is_staff:
        yesterday = (datetime.now() - timedelta(hours=24))
        today = datetime.now()
        search_form = SearchSaleForm()
        if request.method=="POST":
            page = 1
            search_day = request.POST.get('search_day')
            search_month = request.POST.get('search_month')
            search_year = request.POST.get('search_year')
            date = f'{search_year}-{search_month}-{search_day} 00:00:00'
            new_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            #start_time = (new_date + timedelta(hours=8))
            end_time = (new_date + timedelta(hours=23, minutes=59, seconds=59))
            queried_sales = Sale.objects.filter(Q(time_sold__gt=new_date)&Q(time_sold__lt=end_time))
            #print(queried_sales)
            list_revenues = []
            for sale in queried_sales:
                total_revenue = sale.price*sale.quantity
                list_revenues.append(total_revenue)
            total_sale = sum(list_revenues)
            context = {"queried_sales": queried_sales, "search_page": page, "sale": total_sale, 'form':search_form} #, "sales": queried_sales,}
            return render(request, 'app/view_sales.html', context)

        daily_sales = Sale.objects.filter(Q(time_sold=today)|Q(time_sold__gt=yesterday))
        list_revenues = []
        for sale in daily_sales:
            total_revenue = sale.price*sale.quantity
            list_revenues.append(total_revenue)
        total_sale = sum(list_revenues)
        context = {"sales": daily_sales, "sale": total_sale, "form": search_form}
    else:
        return redirect('home')
    return render(request, 'app/view_sales.html', context)

def view_all_sales(request):
    if request.user.is_superuser or request.user.is_staff:
        all_sales = Sale.objects.all()
        context = {"sales": all_sales}
        return render(request, 'app/view_all_sales.html', context)


def add_sales(request):
    if request.user.is_superuser or request.user.is_staff:
        form = SaleForm()
        items = Item.objects.all()
        if request.method == 'POST':              
            item_name = request.POST.get('item')
            quantity = request.POST.get('quantity')
            price = request.POST.get('price')
            item=''
            try:
                item = Item.objects.get(name=item_name)
                if not int(quantity) > item.quantity:
                    Sale.objects.create(item = item, price = price, quantity = quantity)
                    messages.success(request, f'Sales of {item} succesfully recorded')
                    #You can have multiple sales of one item
                    #So we get the most recent sale of an Item by picking the first item in the list returned by the filter method
                    # Since the Sales Model is ordered by time_sold
                    sale = Sale.objects.filter(item=item)[0]
                    x = sale.id
                    y = item.id
                    update_quantity(x, y)
                    
                else:
                    #return HttpResponse('Not Enough Quantity')
                    messages.info(request, "Not Enough Quantity")
        
            except Item.DoesNotExist:
                messages.error(request, 'Check that the details provided in the form are correct')
            context = {"items": items, "form": form}
            return render(request, 'app/add_sales.html', context)
        context = {"items": items, "form": form}
    else:
        return render('home')
    return render(request, 'app/add_sales.html', context)


def add_multiple_sales(request):
    SalesFormSet = modelformset_factory(Sale, fields=('item', 'price', 'quantity'))
    if request.method == 'GET':
        count = request.GET.get('count')
        if count == None:
            count = 0
        else:
            count = int(count)
        # formset_factory do not interact with the model
        items = Item.objects.all()
        SalesFormSet = formset_factory(SaleForm, extra=count)
        multiple_sale_formset = SalesFormSet()
        context = {"formset": multiple_sale_formset, "sales_formset":SalesFormSet, "items": items}
        return render(request, 'app/multiple_sales.html', context )
    else:
        formset = SalesFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                try:
                    if not instance.quantity > instance.item.quantity:               
                        instance.save()
                        messages.info(request, f'Sales of {instance.item.name} succesfuly recorded')
                        update_quantity(instance.id, instance.item.id)
                    else:
                        messages.info(request, "Not Enough Quantity")
                except:
                    messages.error(request, 'Check that the details provided in the form are correct')
        return render(request, 'app/multiple_sales.html')


def item_sale(request, pk):
    item = Item.objects.get(id=pk)
    form = NewSaleForm(initial={"item": item.name})
    sale = Sale.objects.filter(item=item.id)[0]
    if request.method == 'POST':
        filled_form = NewSaleForm(request.POST)
        if filled_form.is_valid():
            item_obj = filled_form.save(commit=False)
            sale = Sale.objects.create(
                item=item_obj,
                price = item_obj.price,
                quantity = item_obj.quantity
            )
            sale = Sale.objects.filter(item=item_obj)[0]
            x = sale.id
            update_quantity(x, pk)
            messages.info(request, f'Sales of {sale.item} succesfully recored')
        #It will never throw an error, becuase it won't allow the submission of empty form
        #Secondly, checking if the sale obj's item received from the form equates to the item's name, will never work
        #Because the instance passed in the form initially will always overide the whatever the user inputs
    context = {"form": form, "item": item}
    return render(request, 'app/item_sale.html', context)


def multiple_item_sales(request, pk):
    SalesFormSet = modelformset_factory(Sale, fields=('item', 'price', 'quantity'))
    item = Item.objects.get(id=pk)
    if request.method == 'GET':
        count = request.GET.get('count')
        if count == None:
            count = 0
        else:
            count = int(count)
        # formset_factory do not interact with the model
        SalesFormSet = formset_factory(NewSaleForm, extra=count)
        multiple_sale_formset = SalesFormSet()
        context = {"formset": multiple_sale_formset, "sales_formset":SalesFormSet, "item": item}
        return render(request, 'app/multiple_item_sales.html', context )
    else:
        formset = SalesFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)


@login_required(login_url='login')
def add_to_cart(request):
    form = SaleForm()
    items = Item.objects.all()
    if request.method == 'POST':
        filled_form = SaleForm(request.POST)
        if filled_form.is_valid:
            item_name = request.POST.get('item')
            quantity = request.POST.get('quantity')
            price = request.POST.get('price')
            item_instance = Item.objects.get(name=item_name)
            check = check_item_quantity(item_instance, quantity)
            if not check == False:
                Cart.objects.create(item= item_instance, user=request.user, price= price, quantity= quantity)
                messages.success(request, 'Item Added to Cart')
            else:
                messages.error(request, 'Not Enough Quantity')
    context = {"form": form, "items": items}
    return render(request, 'app/cart.html', context)



def check_item_quantity(item, quantity):
    if not int(quantity)  > item.quantity:
        return True
    else:
        return False


@login_required(login_url='login')
def add_item_to_cart(request, pk):
    item = Item.objects.get(id=pk)
    form = NewSaleForm(initial={"item": item.name})
    if request.method == 'POST':
        filled_form = NewSaleForm(request.POST)
        if filled_form.is_valid:
            item = request.POST.get('item')
            quantity = request.POST.get('quantity')
            price = request.POST.get('price')
            check = check_item_quantity(item, quantity)
            if not check == False:
                # Note the instance of Item class is passed to the item attribute of the Cart class.
                # This is so because, there is a 1:M relationship between these two classes
                Cart.objects.create(item= item, user= request.user, price= price, quantity= quantity)
                messages.success(request, 'Item Added to Cart')
            else:
                messages.error(request, 'Not Enough Quantity')
    context = {"form": form}
    return render(request, 'app/item_cart.html', context)


@login_required(login_url='login')
def view_cart(request):
    carts = Cart.objects.filter(user=request.user)
    cost = total_cost(carts)
    context = {"carts": carts, "cost": cost}
    return render(request, 'app/view_cart.html', context)


@login_required(login_url='login')
def update_cart(request, pk):
    cart_obj = Cart.objects.get(id=pk)
    if request.user == cart_obj.user:
        form = UpdateCartForm(instance=cart_obj)
        if request.method=='POST':
            filled_form = UpdateCartForm(request.POST, instance=cart_obj)
            if filled_form.is_valid():
                cart_inst = filled_form.save(commit=False)
                cart_inst.item = cart_obj.item
                cart_inst.price = cart_obj.price
                cart_inst.save()
                messages.success(request, 'Quantity successfully updated')
                form = UpdateCartForm()
                context = {"form": form, "cart": cart_obj}
                return render(request, 'app/update_cart.html', context)
        context = {"form": form, "item_name": cart_obj.item, "cart": cart_obj}
    return render(request, 'app/update_cart.html', context)


@login_required(login_url='login')
def delete_cart(request, pk):
    cart_obj = Cart.objects.get(id=pk)
    print(cart_obj)
    if request.method=='POST':
        cart_obj.delete()
        return redirect('view_cart')
    context={"cart": cart_obj}
    return render(request, 'app/delete_cart.html', context)


@login_required(login_url='login')
def checkout(request):
    cart_objs = Cart.objects.filter(user=request.user)
    cart_list = []
    for cart in cart_objs:
        cart_list.append(cart.price * cart.quantity)
    total_cost = sum(cart_list)
    if request.method == 'POST':
        for cart in cart_objs:
            item = Item.objects.get(name=cart.item)
            if not item.quantity < cart.quantity:
                Sale.objects.create(
                    item = cart.item,
                    price = cart.price,
                    quantity = cart.quantity
                )
                sale = Sale.objects.filter(item=cart.item)[0]
                cart_list.append(cart.price * cart.quantity)
                print(max(cart_list))
                update_quantity(sale.id, cart.item.id)
                delete_user_cart(cart)
                messages.success(request, f'{cart.quantity} {cart.item} successfully purchased') 
            else:
                messages.error(request, f'Sorry, not enough quantity of {item.name} at the moment. Please check back later')
            page = 2 
            total_cost = sum(cart_list)
        context = {"cost": total_cost, "page": page}
        return render(request, 'app/checkout_page.html', context)    
    context = {"carts": cart_objs, "cost": total_cost}
    return render(request, 'app/checkout_page.html', context)

@login_required(login_url='login')
def delete_user_cart(obj):
    obj.delete()
    

def total_cost(objs):
    cart_cost_list = []
    for obj in objs:
        cart_cost_list.append(obj.price * obj.quantity)
    total_cost = sum(cart_cost_list)
    return total_cost
