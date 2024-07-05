#build image
# Use an official Python runtime as a parent image
FROM python:3.12.1
# Set the working directory in the container
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY ./requirements.txt /app/
# Install any needed packages specified in requirements.txt
RUN pip install --progress-bar off -r requirements.txt
# Copy the rest of the application
COPY . /app
# Run the application
CMD ["uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]
