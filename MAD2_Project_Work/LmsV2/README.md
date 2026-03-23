# Library Management System V2 - Application Setup Guide

Welcome to the Library Management System V2. This guide will help you set up and run the application on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.x
- Redis Server
- Node.js and npm
- MailHog (for email testing)

## Step 1: Set Up a Python Virtual Environment

Start by creating a Python virtual environment to keep your project dependencies isolated:

```bash
python -m venv env
```
This command will create a folder named `env`, containing the necessary Python executables and libraries for your project.

## Step 2: Activate the Virtual Environment

Activate the virtual environment to ensure that dependencies are installed locally:

- On macOS/Linux:
    ```bash
    source env/bin/activate
    ```

- On Windows:
    ```bash
    .\env\Scripts\activate
    ```

Your terminal prompt should now reflect that you're working within the virtual environment.

## Step 3: Install Required Packages

With the virtual environment active, install the project's dependencies:

```bash
pip install -r requirements.txt
```

This command installs all necessary packages specified in the `requirements.txt` file.

## Step 4: Start the Flask Application

Once dependencies are installed, you can start the Flask application:

```bash
python main.py
```

The Flask server will start and run at `http://127.0.0.1:5000`.

## Step 5: Start Redis Server and MailHog

In a new terminal session, start the Redis server and MailHog for email testing:

- Start Redis:
    ```bash
    redis-server
    ```
- Start MailHog:
    ```bash
    cd ~/go/bin
    ./MailHog
    ```

## Step 6: Run Celery Workers and Beat Scheduler

In a separate terminal session, activate the virtual environment and run Celery:

- For development:
    ```bash
    celery -A main.celery worker --beat --loglevel=info
    ```

- For Production:
    ```bash
    celery -A main.celery worker --loglevel=info
    celery -A main.celery beat --loglevel=info
    ```

This setup integrates Celery with your Flask application, using Redis as the message broker.

## Step 7: Start the Vue.js 3 Server

In a new terminal session, navigate to the `frontend` directory and start the Vue.js development server:

```bash
cd frontend
npm update  # To install/update required packages
npm run serve  # To start the application
```

The Vue.js server will run at `http://127.0.0.1:8080`.

## Step 8: Access the Application

Open your web browser and navigate to: `http://127.0.0.1:8080`

The application comes with 10 pre-registered users:
- Emails: user1@gmail.com to user10@gmail.com
- Password: 12345678

New users can register and log in directly.

**Admin Credentials**

To access the admin interface, use the following credentials:
- Email: admin@gmail.com
- Password: 12345678

Manage the library system as an administrator with these credentials.

## Step 9: Stop the Application

To stop the running application, press Ctrl + C in each terminal window.

## Step 10: Deactivate the Virtual Environment

When you're finished, deactivate the virtual environment:
```bash
deactivate
```
Your terminal prompt will revert to its original state.