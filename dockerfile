# Use an official Python runtime as the parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container
COPY app/ /app/

# Make the Streamlit port available outside this container
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]
