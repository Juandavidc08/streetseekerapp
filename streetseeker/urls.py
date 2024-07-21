from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path('book/<int:place_id>/', views.book_place, name='book_place'),
    path('reservations/', views.reservations, name='reservations'),
    path('edit/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('comment/<int:reservation_id>/', views.add_comment, name='add_comment'),
    path('place/<int:place_id>/comments/', views.view_comments, name='view_comments'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('contact/', views.contact, name='contact'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('book/<int:place_id>/', views.attempt_booking, name='attempt_booking'),
    path('login-required/', views.login_required, name='login_required'),
]
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)