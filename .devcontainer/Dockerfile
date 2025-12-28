FROM osrf/ros:humble-desktop

RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    cmake \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    google-generativeai \
    streamlit \
    opencv-python \
    torch \
    torchvision

WORKDIR /workspace

CMD ["bash"]
