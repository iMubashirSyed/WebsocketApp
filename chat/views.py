from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *

# Create your views here.
@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        room = request.POST.get('room')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, "User does not exist. Please enter a valid username.")
            return redirect('home')
        
        existing_rooms = Room.objects.filter(room_name__icontains=room)
        
        if existing_rooms.exists():
            existing_room = existing_rooms.first()  # Use the first matching room
            return redirect('room',room_name=existing_room.room_name, username=username)
        else:
            messages.error(request, "Room does not exist.") 
            return redirect('home')      
    return render(request, 'home.html')

# @login_required(login_url='login')
# def RoomView(request, room_name, username):
#     existing_room = Room.objects.filter(room_name__icontains=room_name)
#     get_messages = Message.objects.filter(room=existing_room)
#     context = {
#         'messages': get_messages,
#         'room_name': existing_room.room_name,
#         'user':username
#     }
#     return render(request, 'room.html', context)


@login_required(login_url='login')
def RoomView(request, room_name, username):
    # Get existing rooms that match the room name
    existing_rooms = Room.objects.filter(room_name__icontains=room_name)

    # Check if any rooms exist
    if existing_rooms.exists():
        # If there are multiple rooms, you can choose the first one or handle it as needed
        existing_room = existing_rooms.first()  # Use the first matching room

        # Fetch messages for the selected room
        get_messages = Message.objects.filter(room=existing_room)

        context = {
            'messages': get_messages,
            'room_name': existing_room.room_name,
            'user': username
        }
        return render(request, 'room.html', context)
    else:
        messages.error(request, "Room does not exist.")
        return redirect('home')  
    
@login_required(login_url='login')
def create_room(request):
    if request.method == 'POST':
        # username = request.POST.get('username')
        room_name = request.POST.get('room_name')
        
        if Room.objects.filter(room_name=room_name).exists():
            messages.info(request,"Room already exists")
            return redirect('home')

        Room.objects.create(room_name=room_name)
        return redirect('home')
    
    return render(request, 'create_room.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not User.objects.filter(email=email).exists():
            messages.info(request,"Invalid username or password")
            return redirect('login')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            messages.info(request,"Invalid Credentials")
            return redirect('login')
        
        else:
            login(request, user)
            return redirect('home') # redirect to the home page
                
    return render(request,'login.html')

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            messages.info(request,"Email already exists")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.info(request,"Username already exists")
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        # user.set_password(password)
        user.save() 
        messages.info(request,"Account created successfully")
                                       
        return redirect('login') # redirect to home page
                   
    return render(request,'register.html')    

def logout_view(request):
    logout(request)
    return redirect('login')

