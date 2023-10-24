# syntax=docker/dockerfile:1.2
FROM python:latest
# put you docker configuration here 

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r /app/requirements.txt

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8000"]