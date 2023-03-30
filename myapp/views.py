from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
# Create your views here.


def root(request):
    if 'username' in request.session:
        logged_user = User.objects.get(id=request.session['userid'])
        context = {
            'paints': Paint.objects.all(),
            'userpaints': logged_user.purchased_paints.all()
        }

        return render(request, 'index.html', context)
    else:
        return redirect('/loginpage')


def loginpage(request):
    return render(request, 'loginpage.html')


def signup(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/loginpage')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=request.POST['fname'],
                            last_name=request.POST['lname'],
                            email=request.POST['email'],
                            password=pw_hash)
        request.session['username'] = User.objects.last(
        ).first_name + " " + User.objects.last().last_name
        request.session['userid'] = User.objects.last().id

        return redirect('/success')


def signin(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            request.session['username'] = user[0].first_name + \
                ' ' + user[0].last_name
            request.session['userid'] = user[0].id
            return redirect('/success')
        else:
            messages.error(request, "Wrong Password")
            return redirect('/loginpage')
    else:
        messages.error(request, "Email not found in the database")
        return redirect('/loginpage')


def success(request):
    if 'username' in request.session:
        return redirect('/')
    else:
        return redirect('/loginpage')


def logout(request):
    request.session.flush()
    return redirect('/')


def addpainting(request):

    if 'username' in request.session:
        return render(request, "addpaint.html")
    else:
        return redirect('/')


def addpaintsubmit(request):
    errors = Paint.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/addpainting')
    else:
        logged_user = User.objects.get(id=request.session['userid'])
        Paint.objects.create(title=request.POST['title'],
                             desc=request.POST['desc'],
                             price=request.POST['price'],
                             qts=request.POST['qts'],
                             add_by=logged_user)
        return redirect('/')


def edit(request, id):
    if 'username' in request.session:
        context = {
            'paint': Paint.objects.get(id=id)
        }
        return render(request, 'editpaint.html', context)
    else:
        return redirect('/')


def editsubmit(request, id):
    if 'username' in request.session:
        if int(request.session['userid']) == Paint.objects.get(id=id).add_by.id:
            errors = Paint.objects.basic_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/paint/'+str(id)+'/edit')
            else:
                paint = Paint.objects.get(id=id)
                paint.title = request.POST['title']
                paint.desc = request.POST['desc']
                paint.price = request.POST['price']
                paint.qts = qts = request.POST['qts']
                paint.save()
            return redirect('/paint/'+str(id))
    else:
        return redirect('/')


def delete(request, id):
    if 'username' in request.session:
        if int(request.session['userid']) == Paint.objects.get(id=id).add_by.id:
            paint = Paint.objects.get(id=id)
            paint.delete()
            return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')
def paintdetails(request, id):
    if 'username' in request.session:
        paint = Paint.objects.get(id=id)
        numberOfPurchase = len(
            list(Paint.objects.get(id=id).purchased_by.all()))
        paint_qts = int(paint.qts)
        context = {
            'paint': paint,
            'buyable': paint_qts > numberOfPurchase,
            'numberOfPurchase': numberOfPurchase,
        }
        return render(request, 'paint.html', context)
    else:
        return redirect('/')


def buy(request, id):
    paint = Paint.objects.get(id=id)
    logged_user = User.objects.get(id=request.session['userid'])
    paint.purchased_by.add(logged_user)
    return redirect('/')
