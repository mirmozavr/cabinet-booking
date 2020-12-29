from django.shortcuts import render, redirect
from .models import Cabinet, Booking
from datetime import date, datetime


def cabinets(request):
    if request.method == 'GET':
        name = request.user.get_username()
        date_today = date.today()
        cabs = Cabinet.objects.all().order_by('room_number')
        bookings = []
        for cab in cabs:
            bookings.append(Booking.objects.filter(cabinet=cab, booking_end__gte=date_today).order_by('booking_start') or '-')

        cb = list(zip(cabs, bookings))
        date_today = str(date_today)
        context = {'context': cb, 'name': name, 'date': date_today}
        return render(request, 'cabinets.html', context)

    # search for free days logic
    if request.method == 'POST':
        begin = request.POST.get('begin')
        finish = request.POST.get('finish')
        if not begin or not finish or begin > finish:
            return redirect('/cabinets/')

        begin = datetime.strptime(begin, '%Y-%m-%d').date()
        finish = datetime.strptime(finish, '%Y-%m-%d').date()

        asked = Booking(booking_start=begin, booking_end=finish)
        cabs = []
        for cab in Cabinet.objects.all().order_by('room_number'):
            flag = True
            for book in Booking.objects.filter(cabinet=cab):
                if asked.intersect(book):
                    flag = False
                    break
            if flag:
                cabs.append(cab)

        name = request.user.get_username()
        date_today = str(date.today())
        bookings = []
        for cab in cabs:
            bookings.append(Booking.objects.filter(cabinet=cab).order_by('booking_start') or '-')

        cb = list(zip(cabs, bookings))
        context = {'context': cb, 'name': name, 'date': date_today}
        return render(request, 'cabinets.html', context)


def cabinet(request, room, error=''):
    name = request.user.get_username()
    cab = Cabinet.objects.get(room_number=room)
    date_today = date.today()
    booking = Booking.objects.filter(cabinet=cab, booking_end__gte=date_today).order_by('booking_start')
    date_today = str(date_today)
    context = {'cab': cab, 'booking': booking, 'name': name, 'date': date_today, 'error': error}
    return render(request, 'cabinet.html', context)


def book_date(request, room):
    if request.method == 'POST':
        name = request.user
        begin = request.POST.get('begin')
        finish = request.POST.get('finish')
        begin = datetime.strptime(begin, '%Y-%m-%d').date()
        finish = datetime.strptime(finish, '%Y-%m-%d').date()
        if begin > finish:
            return redirect(f'/cabinet/{room}')
        cab = Cabinet.objects.get(room_number=room)

        asked = Booking(booking_start=begin, booking_end=finish)

        for book in Booking.objects.filter(cabinet=cab):
            if asked.intersect(book):
                return cabinet(request, room, error='Date is occupied')

        Booking.objects.create(cabinet=cab, booking_start=begin, booking_end=finish, customer=name)

        return redirect(f'/cabinet/{room}')
