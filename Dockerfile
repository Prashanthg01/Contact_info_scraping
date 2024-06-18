# Use the official Python image from the Docker Hub
FROM python:3.9.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the main.py script
CMD ["python", "single_page_crawl.py"]
