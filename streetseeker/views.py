from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Place, Reservation, Comment, Contact
from .forms import ReservationForm, CommentForm, ContactForm
import random
from random import sample

# Home page view
def home(request):
    return render(request, "home.html")

# Search view to show random places
def search(request):
    all_places = Place.objects.all()

    if len(all_places) >= 3:
        random_places = sample(list(all_places), 3)
    else:
        random_places = all_places

    return render(request, 'search.html', {'random_places': random_places})

# Booking view, requires user to be logged in
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

def attempt_booking(request, place_id):
    if request.user.is_authenticated:
        return redirect('book_place', place_id=place_id)
    else:
        messages.info(request, 'You need to be logged in to book a place.')
        return redirect('login')

# View user's reservations, requires login
@login_required
def reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservations.html', {'reservations': reservations})

# Edit reservation, requires login
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

# Delete reservation, requires login
@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Reservation deleted successfully.')
        return redirect('reservations')
    return render(request, 'delete_reservation.html', {'reservation': reservation})

# Add comment, requires login
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

# View comments for a place
def view_comments(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    reservations = Reservation.objects.filter(place=place)
    comments = Comment.objects.filter(reservation__in=reservations)
    return render(request, 'view_comments.html', {'place': place, 'comments': comments})

# Delete comment, checks user authorization
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    else:
        messages.error(request, 'You are not authorized to delete this comment.')
    return redirect('view_comments', place_id=comment.reservation.place.id)

# Contact form view
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            contact = Contact(name=name, email=email, message=message)
            contact.save()
            return redirect('thank_you')
    else:
        form = ContactForm()
    return render(request, 'contact_form.html', {'form': form})

# Thank you page view
def thank_you(request):
    return render(request, 'thank_you.html')

# Handle access control and redirection to the login page
def handle_unauthenticated_booking(request):
    messages.info(request, 'You need to log in to book a place. Please log in or register to continue.')
    return redirect('login')