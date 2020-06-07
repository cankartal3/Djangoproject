import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Settings, ContactFormuu, ContactFormMessage, UserProfile, FAQ
from turistikmekan.models import Product, Category, Images, Comment


def index(request):
    settings = Settings.objects.get(pk=1)
    sliderdata = Product.objects.filter(status='True').order_by('-id')[:5]
    category = Category.objects.all()

    dayproducts = Product.objects.filter(status='True')[:4]
    lastproducts = Product.objects.filter(status='True').order_by('-id')
    randomproducts = Product.objects.filter(status='True').order_by('?')[:5]
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Login Hatası! Kullanıcı adı ya da şifre yanlış. ")
            return HttpResponseRedirect('/')

    context = {'settings': settings,
               'category':category,
               'page':'home',
               'sliderdata':sliderdata,
               'dayproducts':dayproducts,
               'lastproducts':lastproducts,
               'randomproducts':randomproducts,
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
    settings = Settings.objects.get(pk=1)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id, status='True')
    context = {'products':products,
               'category':category,
               'categorydata':categorydata,
               'settings':settings,
               }
    return render(request,'products.html',context)

def product_detail(request ,id,slug):
    category = Category.objects.all()
    settings = Settings.objects.get(pk=1)
    try:
        product = Product.objects.get(pk=id)
        images = Images.objects.filter(product_id=id,status='True')
        comments = Comment.objects.filter(product_id=id,status='True').order_by('-id') #en son yorumdan itibaren
        avg = Comment.objects.filter(product_id=id, status='True').aggregate(Avg('rate'))
        context = {'product':product,
                   'images':images,
                   'comments':comments,
                   'category':category,
                   'avg':avg,
                   'settings': settings,
                   }
        return render(request,'product_detail.html',context)
    except:
        messages.warning(request, "Hata! İlgili içerik bulunamadı")
        link='/error'
        return HttpResponseRedirect(link)

def product_search(request):
    if request.method == 'POST': #check form post
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query'] #get form data
            catid = form.cleaned_data['catid'] #get form data
            # return HttpResponse(catid)
            if catid == 0:
                products = Product.objects.filter(title__icontains=query) #Select * form product where title like %query%
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)
            #return HttpResponse
            context ={'products':products,
                      'category':category,
                      }
            return render(request, 'products_search.html',context)
        return HttpResponseRedirect('/')


def get_places(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for pl in product:
            product_json = {}
            product_json = pl.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password= password)
            login(request, user)

            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image="images/users/user.png"
            data.save()
            messages.success(request,"Hoş geldiniz. Sitemize başarılı bilr şekilde üye oldunuz. İyi gezmeler.")
            return HttpResponseRedirect("/")

    form = SignUpForm()
    settings = Settings.objects.get(pk=1)
    category = Category.objects.all()
    context = {'category': category,
               'form':form,
               'settings':settings,
               }
    return render(request, 'signup.html', context)


#def bossayfa(request, id):        #project ->urls.py
#    return HttpResponse('Sayfa' + ' ' + str(id))


#def bossayfaa(request):     #home -> urls.py

#    return HttpResponse("Boş Sayfa")


def error(request):
    category = Category.objects.all()
    settings = Settings.objects.get(pk=1)
    context = {
        'category': category,
        'settings':settings,
    }
    return render(request, 'error_page.html', context)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('ordernumber')
    settings = Settings.objects.get(pk=1)
    context = {
        'category': category,
        'faq':faq,
        'settings':settings,
    }
    return render(request, 'faq.html', context)



def visitetouser(request,id):
    category = Category.objects.all()
    profile = User.objects.get(id=id)
    userprofile = UserProfile.objects.get(user_id=id)
    userproducts = Product.objects.filter(user_id=id,status='True')
    settings = Settings.objects.get(pk=1)
    context = {'category': category,
               'profile': profile,
               'userprofile':userprofile,
               'userproducts':userproducts,
               'settings':settings,
               }
    return render(request, 'visit_to_user.html', context)


def login_view(request):
    category = Category.objects.all()
    settings = Settings.objects.get(pk=1)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Login Hatası! Kullanıcı adı ya da şifre yanlış. ")
            return HttpResponseRedirect('/login')
    context = {
        'settings':settings,
        'category': category,
    }
    return render(request, 'login.html', context)


def yurticituristikmekanlar(request):
    settings = Settings.objects.get(pk=1)
    category = Category.objects.all()
    yurticitm = Product.objects.filter(status='True', where='Yurtici').order_by('-id')
    context = {
        'category':category,
        'yurticitm':yurticitm,
        'settings':settings,
    }
    return render(request, 'yurtici.html', context)


def yurtdisituristikmekanlar(request):
    settings = Settings.objects.get(pk=1)
    category = Category.objects.all()
    yurtdisitm = Product.objects.filter(status='True', where='Yurtdisi').order_by('-id')
    context = {
        'category': category,
        'yurtdisitm': yurtdisitm,
        'settings':settings,
    }
    return render(request, 'yurtdisi.html', context)