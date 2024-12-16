# Use an official Python image as a base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install necessary Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port if needed (example: 5000)
# EXPOSE 5000 

# Command to run the application
CMD ["python3", "-m", "TaitanXFun"]