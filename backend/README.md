# Django Project Setup

This project is a Django application. Follow the steps below to set up the project locally and run the development server.

## Prerequisites

Ensure you have the following installed:

- Python (preferably 3.8 or later)
- Django
- A virtual environment (recommended)

## Installation Steps

1. **Clone the repository**:

   Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Boualam3/Booking-restapi.git
   cd Booking-restapi

2. **Create a virtual env**:
    creating venv:
    
    ```bash
    python3 -m venv venv


3. **Install the Requirements**:

    Install the requirements:
    
    ```bash
    pip install -r requirements.txt

4. **Managing the db**:
    Managing db :

    ```bash
    ./manage.py makemigrations
    ./manage.py migrate

5. **Runing the server**:
    runing the server:

    ```bash
    ./manage.py runserver
