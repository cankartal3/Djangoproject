from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from home.models import UserProfile, Settings, AdminMessage
from turistikmekan.models import Category, Comment, Product, ProductForm, ProductImageForm, Images
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    settings = Settings.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category':category,
               'profile':profile,
               'settings':settings,}
    return render(request, 'user_profile.html', context)

@login_required(login_url='/login') #Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) #request.user is user session data
        #"instance=request.user.userprofile" come from "userprofile" model -> OneToOneField relation
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Hesabınız güncellendi!')
            return redirect('/user')

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)  # "userprofile" model -> OneToOneField relation with user
        settings = Settings.objects.get(pk=1)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'settings':settings,
        }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login') #Check login
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) #Important!
            messages.success(request, 'Şifreniz başarılı bir şekilde güncellendi!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below!<br>'+str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        settings = Settings.objects.get(pk=1)
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
        'form':form,'category':category, 'settings':settings,
        })

@login_required(login_url='/login') #Check login
def comments(request):
    settings = Settings.objects.get(pk=1)
    current_userr = request.user
    profile = UserProfile.objects.get(user_id=current_userr.id)
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id).order_by('-id')
    context={
        'category':category,
        'comments':comments,
        'profile':profile,
        'settings':settings,
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login') #Check login
def deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Yorumunuz silindi.')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login') #Check login
def rehberler(request):
    current_userr = request.user
    profile = UserProfile.objects.get(user_id=current_userr.id)
    settings = Settings.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    products = Product.objects.filter(user_id=current_user.id).order_by('-id')

    context = {
        'profile':profile,
        'settings':settings,
        'category': category,
        'products': products,
    }
    return render(request, 'rehberler.html', context)

@login_required(login_url='/login') #Check login
def rehberekle(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Product()  # model ile bağlantı yap
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.category = form.cleaned_data['category']
            data.where = form.cleaned_data['where']
            data.address = form.cleaned_data['address']
            data.howtogo = form.cleaned_data['howtogo']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            if data.image == None:
                data.image = "images/product/product.png"
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()  # veritabanına kaydet
            messages.success(request, 'İçeriğiniz başarılı bir şekilde kaydedildi!')
            return HttpResponseRedirect('/user/rehberler')
        else:
            messages.success(request, 'Content Form Error:' + str(form.errors))
            return HttpResponseRedirect('/user/rehberekle')
    else:
        current_userr = request.user
        profile = UserProfile.objects.get(user_id=current_userr.id)
        settings = Settings.objects.get(pk=1)
        category = Category.objects.all()
        form = ProductForm()
        context = {
            'profile':profile,
            'category': category,
            'form': form,
            'settings':settings,
        }
        return render(request, 'user_rehber_ekle.html', context)

@login_required(login_url='/login') #Check login
def editrehber(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'İçeriğiniz başarılı bir şekilde güncellendi!')
            return HttpResponseRedirect('/user/rehberler')
        else:
            messages.success(request, 'Content Form Error' + str(form.errors))
            return HttpResponseRedirect('/user/editrehber/' + str(id))
    else:
        current_userr = request.user
        profile = UserProfile.objects.get(user_id=current_userr.id)
        settings = Settings.objects.get(pk=1)
        category = Category.objects.all()
        form = ProductForm(instance=product)
        context = {
            'profile':profile,
            'category': category,
            'form': form,
            'settings':settings,
        }
        return render(request, 'user_rehber_ekle.html', context)

@login_required(login_url='/login') #Check login
def deleterehber(request,id):
    current_user = request.user
    Product.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'İçerik silindi.')
    return HttpResponseRedirect('/user/rehberler')

@login_required(login_url='/login') #Check login
def productaddimage(request, id):
    if request.method == 'POST':
        lasturl= request.META.get('HTTP_REFERER')
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.title = form.cleaned_data['title']
            data.product_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Resiminiz başarılı bir şekilde kaydedildi!')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error :' + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        product = Product.objects.get(id=id)
        images = Images.objects.filter(product_id=id)
        form = ProductImageForm()
        context = {
            'product':product,
            'images':images,
            'form':form,
        }
        return render(request, 'product_gallery.html', context)


@login_required(login_url='/login') #Check login
def mesajlar(request):
    current_userr = request.user
    profile = UserProfile.objects.get(user_id=current_userr.id)
    settings = Settings.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    mesajlarim = AdminMessage.objects.filter(user_id=current_user.id).order_by('-id')
    context = {
        'profile':profile,
        'settings':settings,
        'category':category,
        'mesajlarim':mesajlarim,
    }

    return render(request, 'mesajlar.html', context)