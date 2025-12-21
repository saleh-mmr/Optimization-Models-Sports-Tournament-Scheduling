# Base image
FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies (IMPORTANT: libgl1 is required for Gecode)
RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    libgl1 \
    libegl1 \
    libfontconfig1 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libfreetype6 \
    libharfbuzz0b \
    libxkbcommon0 \
    libdrm2 \
    libstdc++6 \
    libgcc-s1 \
    libgpg-error0 \
    && rm -rf /var/lib/apt/lists/*





# Install MiniZinc (x86_64 bundle)
RUN wget https://github.com/MiniZinc/MiniZincIDE/releases/download/2.9.2/MiniZincIDE-2.9.2-bundle-linux-x86_64.tgz \
    && tar -xzf MiniZincIDE-2.9.2-bundle-linux-x86_64.tgz \
    && rm MiniZincIDE-2.9.2-bundle-linux-x86_64.tgz

# Add MiniZinc to PATH
ENV PATH="/MiniZincIDE-2.9.2-bundle-linux-x86_64/bin:${PATH}"

# Install Python dependencies
RUN pip install --no-cache-dir z3-solver

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Default command
CMD ["bash"]
