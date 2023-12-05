# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set default environment variables for RabbitMQ and PostgreSQ

RUN apt-get update
RUN apt-get install -y git

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY req.txt .

# Install any needed packages specified in req.txt
RUN pip install -r req.txt


# Copy the rest of the application code into the container
COPY . .

# Install fastapi-template
RUN pip install git+https://github.com/Myortv/fastapi-plugins.git@dev

# Expose the port your FastAPI app will run on
EXPOSE 8001

# Command to start your FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4", "--log-config", "app/core/log.config"]
