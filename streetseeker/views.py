from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Place, Reservation, Comment
from .forms import ReservationForm, CommentForm, ContactForm
import random
from random import sample

# Create your views here.

def home(request):
    return render(request, "home.html")

def search(request):
    # Get all places from the database
    all_places = Place.objects.all()

    # Sample three random places if there are at least three places in the database
    if len(all_places) >= 3:
        random_places = sample(list(all_places), 3)
    else:
        random_places = all_places

    return render(request, 'search.html', {'random_places': random_places})

@login_required
def book_place(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('reservations')
    else:
        form = ReservationForm(initial={'place': place})
    return render(request, 'book.html', {'form': form, 'place': place})

@login_required
def reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservations.html', {'reservations': reservations})

@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservations')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'edit_reservation.html', {'form': form})

@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        return redirect('reservations')
    return render(request, 'delete_reservation.html', {'reservation': reservation})

@login_required
def add_comment(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.reservation = reservation
            comment.user = request.user
            comment.save()
            return redirect('reservations')
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form, 'reservation': reservation})

def view_comments(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    
    # Get reservations associated with the place
    reservations = Reservation.objects.filter(place=place)
    
    # Filter comments based on reservations
    comments = Comment.objects.filter(reservation__in=reservations)

    return render(request, 'view_comments.html', {'place': place, 'comments': comments})

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the user is the owner of the comment
    if comment.user == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    else:
        messages.error(request, 'You are not authorized to delete this comment.')
    
    return redirect('view_comments', place_id=comment.reservation.place.id)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # For simplicity, we'll assume printing to console for demonstration
            print(f"Name: {name}\nEmail: {email}\nMessage: {message}")
            return render(request, 'thank_you.html')
    else:
        form = ContactForm()
    return render(request, 'contact_form.html', {'form': form})
