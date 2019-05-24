from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from .models import Users, UsersManager, Trips
from django.contrib import messages

def index(request):
    return render(request, "trip_app/index.html")

def dashboard(request):
    if not 'userid' in request.session:
        return redirect('/notlogged')
    creator = Users.objects.get(id=request.session['userid'])
    mytrips = Trips.objects.filter(creator=request.session['userid']) | Trips.objects.filter(attendees=creator.id)
    ids_to_exclude = [x.id for x in mytrips]
    othertrips = Trips.objects.exclude(id__in = ids_to_exclude)
    context = {
        "mytrips": mytrips,
        "othertrips": othertrips
    }
    return render(request, "trip_app/dashboard.html", context)

def logout(request):
    request.session.flush()
    return redirect("/")

def register(request):
    if request.method == "POST":
        f_name = request.POST["f_name"]
        l_name = request.POST["l_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm = request.POST["confirm"]
        errors = Users.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        else:
            hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            new_user = Users.objects.create(f_name=f_name,l_name=l_name,email=email,password=hash_pw)
            request.session['f_name'] = f_name
            request.session['userid'] = new_user.id
        return redirect("/dashboard")

def login(request):
    errors = {}
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = Users.objects.get(email=email)
        except:
            errors['login'] = "Couldn't login"
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        if bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['userid'] = user.id
            request.session['f_name'] = user.f_name
            return redirect("/dashboard")
        else:
            errors['login'] = "Couldn't login"
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')


def trip(request,id):
    if not 'userid' in request.session:
        return redirect('/notlogged')
    my_trip = Trips.objects.get(id=id)
    attendees = my_trip.attendees.all()
    context = {
        "trip": my_trip,
        "attendees": attendees
    }
    print(context.values())
    return render(request, "trip_app/trip.html", context)

def edit(request,id):
    if not 'userid' in request.session:
        return redirect('/notlogged')
    my_trip = Trips.objects.get(id=id)
    start = str(my_trip.start)
    end = str(my_trip.end)
    context = {
        "trip" : my_trip,
        "start" : start,
        "end" : end
    }
    return render(request, "trip_app/edit.html", context)

def doedit(request):
    if request.method == "POST":
        destination = request.POST["destination"]
        start = request.POST["start"]
        end = request.POST["end"]
        plan = request.POST["plan"]
        id = request.POST['id']
        errors = Trips.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/edit/' + id)
        else:
            user = Users.objects.get(id=request.session['userid'])
            this_trip = Trips.objects.get(id=id)
            this_trip.destination = destination
            this_trip.start = start
            this_trip.end = end
            this_trip.plan = plan
            this_trip.save()
    return redirect("/dashboard")

def donewtrip(request):
    if request.method == "POST":
        destination = request.POST["destination"]
        start = request.POST["start"]
        end = request.POST["end"]
        plan = request.POST["plan"]
        errors = Trips.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/newtrip')
        else:
            user = Users.objects.get(id=request.session['userid'])
            Trips.objects.create(destination=destination,start=start,end=end,plan=plan,creator=user)
    return redirect("/dashboard")


def newtrip(request):
    if not 'userid' in request.session:
        return redirect('/notlogged')
    return render(request, "trip_app/newtrip.html")

def remove(request, id):
    trip_to_delete = Trips.objects.get(id=id)
    trip_to_delete.delete()
    return redirect("/dashboard")

def join(request, id):
    this_trip = Trips.objects.get(id=id)
    this_user = Users.objects.get(id=request.session['userid'])
    this_trip.attendees.add(this_user)
    return redirect("/dashboard")

def cancel(request, id):
    this_trip = Trips.objects.get(id=id)
    this_user = Users.objects.get(id=request.session['userid'])
    this_trip.attendees.remove(this_user)
    return redirect("/dashboard")

def notlogged(request):
    errors={}
    errors['login'] = "Not logged in"
    for key, value in errors.items():
        messages.error(request, value, extra_tags=key)
    return redirect('/')

