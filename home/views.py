import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import Menu, Content, CImage, Commentcontent
from home.forms import SearchForm, SignUpForm
from home.models import Settings, ContactFormuu, ContactFormMessage, UserProfile, FAQ
from turistikmekan.models import Product, Category, Images, Comment


def index(request):
    settings = Settings.objects.get(pk=1)
    sliderdata = Product.objects.filter(status='True').order_by('-id')[:5]
    category = Category.objects.all()
    menu = Menu.objects.all()
    dayproducts = Product.objects.filter(status='True')[:4]
    lastproducts = Product.objects.filter(status='True').order_by('-id')[:9]
    randomproducts = Product.objects.filter(status='True').order_by('?')[:5]
    duyuru = Content.objects.filter(status='True', type='duyuru').order_by('-id')[:3]
    etkinlik = Content.objects.filter(status='True', type='etkinlik').order_by('-id')[:3]
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
               'menu':menu,
               'duyuru':duyuru,
               'etkinlik':etkinlik
               }

    return render(request, 'index.html', context)

def hakkimizda(request):
    menu = Menu.objects.all()
    category = Category.objects.all()
    settings = Settings.objects.get(pk=1)
    context = {'settings': settings,'menu':menu, 'category':category,'page':'hakkimizda'}
    return render(request, 'hakkimizda.html', context)

def referanslarimiz(request):
    menu = Menu.objects.all()
    category = Category.objects.all()
    settings = Settings.objects.get(pk=1)
    context = {'settings': settings,'menu':menu, 'page':'referanslarimiz','category':category}
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
    menu = Menu.objects.all()
    category = Category.objects.all()
    settings = Settings.objects.get(pk=1)
    form = ContactFormuu()
    context = {'settings': settings,'menu':menu, 'form':form,'category':category}
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
    menu = Menu.objects.all()
    category = Category.objects.all()

    try:
        product = Product.objects.get(pk=id)
        images = Images.objects.filter(product_id=id)
        comments = Comment.objects.filter(product_id=id,status='True').order_by('-id') #en son yorumdan itibaren
        context = {'product':product,
                   'images':images,
                   'comments':comments,
                   'category':category,
                   'menu':menu}
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
    category = Category.objects.all()
    context = {'category': category,
               'form':form,
               }
    return render(request, 'signup.html', context)


def menu(request, id):
    try:
        content= Content.objects.get(menu_id=id)
        link ='/content/'+str(content.id)+'/menu'
        return HttpResponseRedirect(link)
    except:
        messages.warning(request, "Hata! İlgili içerik bulunamadı")
        link='/error'
        return HttpResponseRedirect(link)

def contentdetail(requset, id, slug):
    commentscontent = Commentcontent.objects.filter(content_id=id, status='True').order_by('-id')  # en son yorumdan itibaren
    category = Category.objects.all()
    menu = Menu.objects.all()

    try:
        content = Content.objects.get(pk=id)
        image = CImage.objects.filter(content_id=id)
        comment = Comment.objects.filter(product_id=id, status='True')
        context = {
            'content':content,
            'category':category,
            'menu':menu,
            'image':image,
            'comment':comment,
            'commentscontent':commentscontent
        }
        return render(requset, 'content_detail.html', context)
    except:
        messages.warning(requset, "Hata! İlgili içerik bulunamadı")
        link='/error'
        return HttpResponseRedirect(link)

#def bossayfa(request, id):        #project ->urls.py
#    return HttpResponse('Sayfa' + ' ' + str(id))


#def bossayfaa(request):     #home -> urls.py

#    return HttpResponse("Boş Sayfa")


def error(request):
    category = Category.objects.all()
    menu = Menu.objects.all()

    context = {
        'category': category,
        'menu': menu,
    }
    return render(request, 'error_page.html', context)


def faq(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
    faq = FAQ.objects.all().order_by('ordernumber')
    context = {
        'category': category,
        'menu': menu,
        'faq':faq,
    }
    return render(request, 'faq.html', context)



def visitetouser(request,id):
    category = Category.objects.all()
    profile = User.objects.get(id=id)
    userprofile = UserProfile.objects.get(user_id=id)
    context = {'category': category,
               'profile': profile,
               'userprofile':userprofile,
               }
    return render(request, 'visit_to_user.html', context)