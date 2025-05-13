# Fetching an image
FROM python:latest

# Setting the working directory inside the image
WORKDIR /app

# Copying the requirements.txt and placing it inside the image.
COPY requirements.txt .

# Updating pip
RUN pip install --upgrade pip

# Installing libraries
RUN pip install -r requirements.txt

# Attaching the current directory to the volume.
COPY . .
