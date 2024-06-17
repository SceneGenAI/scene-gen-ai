# Use the NVIDIA CUDA runtime as a base image with CUDA 12.4
FROM nvidia/cuda:12.1.0-runtime-ubuntu20.04

# Set the working directory in the container
WORKDIR /app

# Set environment variable to non-interactive
ENV DEBIAN_FRONTEND=noninteractive

# Set the timezone (change to your desired timezone)
ENV TZ=UTC

# Install system dependencies including pip3
RUN apt-get update && apt-get install -y \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version
RUN pip3 install --upgrade pip

# Install PyTorch with CUDA support
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu121
# Install other Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install -qq -U diffusers datasets transformers accelerate ftfy pyarrow==9.0.0

RUN pip3 install tensorflow[and-cuda]

RUN pip3 install typing-extensions --upgrade


# Copy the current directory contents into the container at /app
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV ENV_VAR_NAME value

# Run uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
