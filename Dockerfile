# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set default environment variables for RabbitMQ and PostgreSQL
ENV RABBITMQ_HOST test.goloneil.org
ENV RABBITMQ_PORT 5672
ENV POSTGRES_HOST test.goloniel.org
ENV POSTGRES_PORT 5432

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY req.txt .

# Install any needed packages specified in req.txt
RUN pip install -r req.txt


# Copy the rest of the application code into the container
COPY . .

# Install fastapi-template
RUN pip install https://github.com/Myortv/fastapi-plugins.git

# Expose the port your FastAPI app will run on
EXPOSE 8000

# Command to start your FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--log-config", "app/core/log.config"]