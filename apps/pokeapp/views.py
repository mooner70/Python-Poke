from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *
import bcrypt

def index(request):
    return redirect("/main")
def main(request):
    return render (request, "index.html")
def logout(request):
    request.session.flush()
    return redirect('/')
def loggedin(request):
    return redirect("/pokes")


    
def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect("/")
    else:
        pw = request.POST["password"]
        hash1 = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        b = User.objects.create(name=request.POST["name"], alias=request.POST["alias"], email=request.POST["email"], password=hash1, dob=request.POST["dob"])
        request.session['alias'] = request.POST["alias"]
        request.session["user_id"] = b.id
        return redirect("/loggedin")    
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect("/")
    else:
        user = User.objects.get(email = request.POST["email"])
        request.session['alias'] = user.alias
        request.session["user_id"] = user.id
        return redirect("/loggedin")
def pokes(request):
  users = User.objects.exclude(id=request.session['user_id'])
  pokes = User.objects.all()
  context = {
    "users" : users,
    "pokes" : pokes
  }
  return render(request, "pokes.html", context)
def poke(request, id):
  user = User.objects.get(id=request.session["user_id"])
  poker = User.objects.get(id=id)
  user.pokers.add(poker)
  poker.pokes +=1
  poker.save()
  return redirect("/pokes")




# def friends(request):
#     me = User.objects.get(id=request.session["user_id"])
#     people = User.objects.exclude(friend_of=me).exclude(id=request.session["user_id"])
#     friend = me.friend_of.all()
#     context = {
#         "people" : people,
#         "friends" : friend
#     }
#     return render(request, 'friends.html', context)
# 
# def add_to_list(request, id):
#     user = User.objects.get(id=request.session["user_id"])
#     friend = User.objects.get(id=id)
#     user.friend_of.add(friend)
#     return redirect('/friends')
# def remove_from_list(request, id):
#     user = User.objects.get(id=request.session["user_id"])
#     friend = User.objects.get(id=id)
#     user.friend_of.remove(friend)
#     return redirect('/friends')
