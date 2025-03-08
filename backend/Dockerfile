# Dockerfile for Backend (Django)
FROM python:3.12

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the backend code
COPY . .

# Run migrations and collect static files
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Start the Django app with Gunicorn
CMD ["gunicorn", "BookingApplication.wsgi:application", "--bind", "0.0.0.0:$PORT"]

