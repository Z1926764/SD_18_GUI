# Project Overview
This project encompasses the UI portion of the design. 
- The `app/` directory contains the bulk of the UI code. 
- `db.sqlite3` is the SQLite database that contains the pressure data
- Celery is being used in conjuction with Redis to automate the pressure collection process and send the relevant data from Python to JavaScripts
- Run the command `python manage.py runserver` within the project directory to begin the Django server locally and navigate to `localhost:8000` to interact with the UI
- Run the command `python -m celery -A app worker --beat` within the project directory to begin the automated process of collecting and transferring pressure data
- Run the command `sudo pigipod` to start the GPIO daemon which allows
PWM signaling  

# App Specifics
## Modifying the UI
The code that determines the style and function of the UI is contained with the `app/templates` and `app/static` directories. `app/views.py` defines the HTML templates that are served as HTTP responses when navigating to the URLs listed in `app/urls.py`. `project/urls.py` defines the URL for the preexisting admin page and links to `app/urls.py` for any other URLs.

## Settings
The settings for this project can be modified within `project/settings.py`

## Automated Tasks
The `apps/tasks.py` file determines the tasks that Celery will run and `apps/celery.py` sets the schedule for how often those tasks run and initializes some of Celery's settings
