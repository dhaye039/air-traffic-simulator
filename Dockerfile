# Use an official Python 3.11 image as the base image
FROM python:3.11-slim-buster

# Set the working directory inside the container
WORKDIR /backend

# Copy the requirements file into the container
COPY requirements.txt /backend/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY ./backend /backend/

# Expose the port on which the Django app will run
EXPOSE 8000

# Set the default command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
