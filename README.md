FaceTrack Backend (Django)

Setup (local):
1. Create a Python venv and activate it:
   python3 -m venv .venv
   source .venv/bin/activate
2. Install dependencies:
   pip install -r requirements.txt
3. Copy `.env.example` to `.env` and set `DATABASE_URL` for your Postgres instance.
4. Run migrations and create superuser:
   python manage.py migrate
   python manage.py createsuperuser
5. Run server:
   python manage.py runserver

Database name suggestion: facetrack_db
