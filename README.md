# Appointment-App

install python3.8


python3 -m venv env

source env/bin/activate

go to clone project : run = "cd Appointment-App/appointment_site/"

run "pip install -m requirements.txt

run "python manage.py migrate"

run "python manage.py createsuperser"

run "python manage.py runserver"

ensure server is running 127.0.0.1:8000

opne postman and start hitting api with help documnet and info send in email

Note: For run unit tests : run "python manage.py test user_management"
