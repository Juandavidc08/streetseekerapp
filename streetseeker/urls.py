from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name ="home"),
    path("search/", views.search, name="search"),
    path('book/<int:place_id>/', views.book_place, name='book_place'),
    path('reservations/', views.reservations, name='reservations'),
    path('edit/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('comment/<int:reservation_id>/', views.add_comment, name='add_comment'),
    
]