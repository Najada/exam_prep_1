from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip
# Create your views here.
def index(request):
    if 'user_id' in request.session:
        return redirect('/success')
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/success')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    # Get all the id's of the trips that the current user is joined
    ids = []
    for trip in user.trips.all():
        ids.append(trip.id)
        
    trips = Trip.objects.exclude(id__in=ids)
    
    context = {
        'user': user,
        'trips' : trips
    }
    return render(request, 'success.html', context)

# Display Travel place create page

def add(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'trip.html', context={})

def save(request):
    #if 'user_id' not in request.session:
    #    return redirect('/')
    errors = Trip.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/travels/add')
    
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.create(
        destination=request.POST['destination'],
        description=request.POST['description'],
        start_date=request.POST['start_date'],
        end_date=request.POST['end_date'],
        user_id=request.session['user_id']
    )
    user.trips.add(trip)
    return redirect('/success')

def join(request, id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=id)
    user.trips.add(trip)
    return redirect('/success')

def destination(request, id):
    trip = Trip.objects.get(id=id)
    context = {
        'trip': trip
    }
    return render(request, 'show.html', context)





