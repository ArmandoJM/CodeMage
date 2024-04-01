# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Set environment variables.
# Python won't try to write .pyc files on the import of source files.
# Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory.
WORKDIR /code

# Install dependencies.
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project code.
COPY . /code/

# Expose the port the app runs on.
EXPOSE 5000

# Run the application.
CMD ["python", "app.py"]
