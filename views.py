from django.shortcuts import render, redirect
from .models import User, Wish
from django.contrib import messages
# Create your views here.
def index(request):
    index = {
        'title' : 'Welcome to Python Belt',
        'user' : User.objects.get(pk=1),
        'mywishs' : Wish.objects.all().order_by('id').reverse(),
        'allwishs' : Wish.objects.all().order_by('id').reverse(),
    }
    return render(request, 'WishList/index.html', index)

def register(request):
    if request.method == 'POST':
        print request.POST
        response_from_models = User.objects.register(request.POST)
        if not response_from_models['status']:
            for error in response_from_models['errors']:
                messages.error(request, error)
            return redirect('WishList:register')
        else:
            request.session['user_id'] = response_from_models['user'].id
            return redirect('WishList:addWish')
    else:
        register = {
            'title' : 'Welcome to register',
        }
        return render(request, 'WishList/register.html', register)

def login(request):
    if request.method == 'POST':
        print request.POST
        response_from_models = User.objects.login(request.POST)
        if not response_from_models['status']:
            for error in response_from_models['errors']:
                messages.error(request, error)
            return redirect('WishList:login')
        else:
            request.session['user_id'] = response_from_models['user_id']
            return redirect('WishList:index')
    else:
        login = {
            'title' : 'Welcome to login',
        }
        return render(request, 'WishList/login.html', login)

def addWish(request):
    if request.method == 'POST':
        print request.POST
        if not 'user_id' in request.session:
            messages.error(request, 'Must be login!')
            return redirect('WishList:login')
        else:
            Wish.objects.addWish(request.POST)
            return redirect('WishList:index')
    else:
        addWish = {
            'title' : 'Create a New Wish List Item',
        }
        return render(request, 'WishList/addWish.html', addWish)

def delWish(request, id):
    Comment.objects.delWish(request.POST)
    return redirect('WishList:index')

def mvWish(request):
    if request.method == 'POST':
        print request.POST
        if not 'user_id' in request.session:
            messages.error(request, 'Must be login!')
            return redirect('WishList:login')
        else:
            Wish.objects.mvWish(request.POST)
            return redirect('WishList:index')

def showWish(request, id):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be login!')
        return redirect('WishList:login')
    else:
        showWish = {
            'title' : 'Show a wish',
            'wishs' : Wish.objects.all().filter(id = 'id'),
        }
    return render(request, 'WishList/showWish.html', showWish)

def logOut(request):
    request.session.clear()
    return redirect('WishList:index')
