from multiprocessing import context
import bcrypt
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User,Tree

# Create views here!
def index(request):
    return render(request, "index.html")

def create_user(request):
    errors = User.objects.new_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/")

    else:
        newFirstName = request.POST["first_name"]
        newLastName = request.POST["last_name"]
        newEmail = request.POST["email"]
        password = request.POST["password"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name=newFirstName, last_name=newLastName, email=newEmail, password=pw_hash)
        request.session["user_id"] = new_user.id
        return redirect("/dashboard")

def success(request):
    if "user_id" not in request.session:
        return redirect("/")
    context = {
        "new_user" : User.objects.get(id=request.session["user_id"]),
        "all_trees": Tree.objects.all(),
    }
    return render(request, "success.html", context)

def proc_login(request):
    if request.method != "POST":
        return redirect("/")
    valid = User.objects.login_validator(request.POST)
    if len (valid["errors"]) > 0:
        for key, value in valid["errors"].items():
            messages.error(request,value)
        return redirect("/")
    else:
        request.session["user_id"] = valid["user"].id
        return redirect ("/dashboard")
    
    

def logout(request):
    request.session.clear()
    return redirect ("/")

def plant(request):
    if "user_id" not in request.session:
        return redirect("/")
    context = {
        "new_user" : User.objects.get(id=request.session["user_id"]),
        "all_trees": Tree.objects.all(),
    }
    return render(request,'tree.html',context)

def addplant(request):
    errors = Tree.objects.tree_validation(request.POST)
    the_user = User.objects.get(id=request.session["user_id"])
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/plant")
    else :
        species_new = request.POST["species"]
        location_new = request.POST["location"]
        reason_new = request.POST["reason"]
        date_planted_new = request.POST["date_planted"]
        planted_by_new = the_user
        tree= Tree.objects.create(species = species_new,
        location = location_new,
        reason = reason_new,
        date_planted = date_planted_new,
        planted_by = planted_by_new)
        tree.save()
        return redirect('/dashboard')

def account(request):
    if "user_id" not in request.session:
        return redirect("/")
    context = {
        "new_user" : User.objects.get(id=request.session["user_id"]),
        "all_trees": Tree.objects.all(),
    }
    return render(request, 'account.html', context)


def edit(request,id):
    if "user_id" not in request.session:
        return redirect("/")
    context = {
    "new_user" : User.objects.get(id=request.session["user_id"]),
    'my_tree':Tree.objects.get(id=id),
    'datee':Tree.objects.get(id=id).date_planted.strftime('%Y-%m-%d')
    }
    return render(request, 'edit.html', context)

def edit_tree(request):
    errors = Tree.objects.tree_validation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/")
    else :
        tree_id = request.POST['tree_idh']
        tree = Tree.objects.get(id = tree_id)
        species_new = request.POST["species"]
        location_new = request.POST["location"]
        reason_new = request.POST["reason"]
        date_planted_new = request.POST["date_planted"]
        tree.species = species_new
        tree.location = location_new
        tree.reaseon = reason_new
        tree.date_planted = date_planted_new
        tree.save()
        return redirect('/dashboard')

def show(request,id):
    if "user_id" not in request.session:
        return redirect("/")
    context = {
    "new_user" : User.objects.get(id=request.session["user_id"]),
    'my_tree':Tree.objects.get(id=id),
    }
    return render(request,'show.html',context)

def visit(request,id):
    user = User.objects.get(id=request.session["user_id"])
    tree = Tree.objects.get(id=id)
    user.visitors.add(tree)
    return redirect(f'/show/{id}')

def delete(request,id):
    x = Tree.objects.get(id=id)
    x.delete()
    return redirect('/account')