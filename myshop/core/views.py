from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.db.models import Count,Prefetch
from django.core.paginator import Paginator
from .form import ReviewForm
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

# Create your views here.

def index(request):
    offer=Offerproduct.objects.filter(is_active=True)
    category=Category.objects.annotate(SubCategory_count=Count('subcategory')).prefetch_related(Prefetch('subcategory_set',queryset=SubCategory.objects.annotate(product_count=Count('product'))))
    
    subcategory_id=request.GET.get('subcategory')
    min=request.GET.get('min')
    max=request.GET.get('max')
    if subcategory_id and min and max:
        product=Product.objects.filter(subcategory=subcategory_id,price__range=(min,max))
    elif subcategory_id:
        product=Product.objects.filter(subcategory=subcategory_id)
    else:
        product=Product.objects.all()

    paginator=Paginator(product,6)
    n_page=request.GET.get('page')
    data=paginator.get_page(n_page)
    total=data.paginator.num_pages

    context={
        'offer':offer,
        'category':category,
        'product':product,
        'data':data,
        'num':[i+1 for i in range(total)]
    }
    return render(request,'core/index.html',context)

    
def product_detail(request,id):
    product=get_object_or_404(Product,id=id)
    reviews=product.reviews.all()
    review_count=product.reviews.all().count()

    form=ReviewForm()
    if request.method == 'POST':
        form=ReviewForm(data=request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.product=product
            review.user=request.user
            review.save()
            return redirect('product_detail',id=product.id)
    context={
        'product':product,
        'form':form,
        'reviews':reviews,
        'range':range(1,6),
        'review_count':review_count
    }

    return render(request,'core/product_detail.html',context)


'''
Cart 

'''
@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_detail(request):
    return render(request, 'core/cart.html')