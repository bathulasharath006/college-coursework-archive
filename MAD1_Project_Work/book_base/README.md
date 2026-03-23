# Library Management System Application Setup Guide

This guide will walk you through the steps to set up and run the Library Management System application on your local machine.

## Step 1: Create a Python Virtual Environment

First, let's create a Python virtual environment to isolate our project dependencies.

```bash
python -m venv env
```

This command creates a folder named `env` which contains all the necessary Python executables and libraries for our project.

## Step 2: Activate the Virtual Environment

Next, activate the virtual environment to ensure that the dependencies installed for this project do not conflict with other Python projects on your system.

```bash
source env/bin/activate
```

Once activated, your terminal prompt should change to indicate that you are now working within the virtual environment.

## Step 3: Install the Required Packages

After creating the virtual environment, install the required Python packages listed in the `requirements.txt` file to avoid deprecation errors.

```bash
pip install -r requirements.txt
```

This command will download and install all the necessary dependencies for the Library Management System.

## Step 4: Start the Application

With the virtual environment activated and dependencies installed, you can now start the Library Management System application.

```bash
python main.py
```

Running this command will launch the application, allowing you to interact with it through your terminal.

## Step 5: Access the Application

After starting the application, open your web browser and enter the following URL: [http://127.0.0.1:8080](http://127.0.0.1:8080)

By default, 10 users are already registered in the Library. Here are their credentials:
- Email: user1@gmail.com to user10@gmail.com
- Password: 12345678

New users can register and login directly.

## Admin Credentials

To access the admin account, use the following credentials:
- User ID: admin@gmail.com
- Password: 12345678

You can manage the library system as an administrator using these credentials.

## Step 6: Stopping the Application

To stop the application, simply press `Ctrl + C` in your terminal. This will terminate the running process.

## Step 7: Exit the Virtual Environment

Once you're done using the application, you can exit the virtual environment to return to your system's default Python environment.

```bash
deactivate
```

This command will deactivate the virtual environment, and your terminal prompt will revert to its original state.
