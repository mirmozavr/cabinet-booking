from django.urls import path
from workspace.views import cabinet, cabinets, book_date

urlpatterns = [
    path('cabinets/', cabinets),
    path('cabinet/<room>/', cabinet),
    path('book-date/<room>', book_date)
]