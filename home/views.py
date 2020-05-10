from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Settings, ContactFormuu, ContactFormMessage
from turistikmekan.models import Product, Category, Images, Comment


def index(request):
    settings = Settings.objects.get(pk=1)
    sliderdata = Product.objects.all().order_by('-id')
    category = Category.objects.all()
    integer = 1
    dayproducts = Product.objects.all()[:4]
    lastproducts = Product.objects.all().order_by('-id')[:9]
    randomproducts = Product.objects.all().order_by('?')[:5]


    context = {'settings': settings,
               'category':category,
               'page':'home',
               'sliderdata':sliderdata,
               'integer':integer,
               'dayproducts':dayproducts,
               'lastproducts':lastproducts,
               'randomproducts':randomproducts
               }

    return render(request, 'index.html', context)

def hakkimizda(request):
    category = Category.objects.all()
    settings = Settings.objects.get(pk=1)
    context = {'settings': settings, 'category':category,'page':'hakkimizda'}
    return render(request, 'hakkimizda.html', context)

def referanslarimiz(request):
    category = Category.objects.all()
    settings = Settings.objects.get(pk=1)
    context = {'settings': settings, 'page':'referanslarimiz','category':category}
    return render(request, 'referanslarimiz.html', context)

def iletisim(request):

    if request.method == 'POST':  # form post edildiyse
        form = ContactFormuu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name']  # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veri tabanına kaydet
            messages.success(request, "Mesajınız başarılı bir şekilde gönderilmiştir. Teşekkür ederiz.")
            return HttpResponseRedirect('/iletisim')
    category = Category.objects.all()
    settings = Settings.objects.get(pk=1)
    form = ContactFormuu()
    context = {'settings': settings, 'form':form,'category':category}
    return render(request, 'iletisim.html', context)

def category_products(request ,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)
    context = {'products':products,
               'category':category,
               'categorydata':categorydata}
    return render(request,'products.html',context)

def product_detail(request ,id,slug):
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True').order_by('-id') #en son yorumdan itibaren
    context = {'product':product,
               'images':images,
               'comments':comments}
    return render(request,'product_detail.html',context)