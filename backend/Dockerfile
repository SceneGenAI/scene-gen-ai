# backend/Dockerfile

# Use the NVIDIA CUDA runtime as a base image
#FROM nvidia/cuda:11.2.2-cudnn8-runtime-ubuntu20.04
FROM python:3.9


# Set the working directory in the container
WORKDIR /app

# Install dependencies
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    python3.9 \
#    python3-pip \
#    && rm -rf /var/lib/apt/lists/*

# Install PyTorch with CUDA support
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu118


# Install other Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt


# Copy the current directory contents into the container at /app
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV ENV_VAR_NAME value

# Run uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
