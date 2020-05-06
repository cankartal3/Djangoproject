from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Settings, ContactFormuu, ContactFormMessage
from turistikmekan.models import Product, Category


def index(request):
    settings = Settings.objects.get(pk=1)
    sliderdata = Product.objects.all()
    category = Category.objects.all()
    integer = 0
    context = {'settings': settings,
               'category':category,
               'page':'home',
               'sliderdata':sliderdata,
               'integer':integer}

    return render(request, 'index.html', context)

def hakkimizda(request):
    settings = Settings.objects.get(pk=1)
    context = {'settings': settings, 'page':'hakkimizda'}
    return render(request, 'hakkimizda.html', context)

def referanslarimiz(request):
    settings = Settings.objects.get(pk=1)
    context = {'settings': settings, 'page':'referanslarimiz'}
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

    settings = Settings.objects.get(pk=1)
    form = ContactFormuu()
    context = {'settings': settings, 'form':form}
    return render(request, 'iletisim.html', context)

def category_products(request ,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)
    context = {'products':products,
               'category':category,
               'categorydata':categorydata}
    return render(request,'products.html',context)