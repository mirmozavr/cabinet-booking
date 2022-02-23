FROM python:3.8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install -r requirements.txt
RUN python manage.py migrate

RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'adminEmail', 'admin')" | python manage.py shell

EXPOSE 8000
