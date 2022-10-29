FROM nvidia/cuda:11.2.0-cudnn8-devel-ubuntu18.04
ENV DEBCONF_NOWARNINGS yes \
    DEBIAN_FRONTEND=noninteractive
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Install packages from apt
RUN sed -i "s/archive.ubuntu/mirror.kakao/g" /etc/apt/sources.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
    libgl1-mesa-dev libglib2.0-0 libsm6 libxrender1 libxext6 \
    software-properties-common sudo git curl unzip wget locales \
    python3-pip python3-dev \
    tree vim \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists

# Install packages of encoder4editing & StyleCLIP
RUN python3 -m pip install --upgrade pip \
 && python3 -m pip uninstall tensorflow -y \
 && python3 -m pip install awslambdaric \
 && python3 -m pip install setuptools wheel cmake cython \
 && python3 -m pip install nvidia-pyindex \
 && python3 -m pip install nvidia-tensorflow==1.15.4 \
 && python3 -m pip install nvidia-tensorboard \
 && python3 -m pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 \
    -f https://download.pytorch.org/whl/torch_stable.html \
 && python3 -m pip install ftfy regex tqdm requests pandas opencv-python matplotlib \
 && python3 -m pip install git+https://github.com/openai/CLIP.git \
 && python3 -m pip install boto3 pyyaml rich
# && python3 -m pip cache purge

# Set localtime
RUN locale-gen "en_US.UTF-8"
ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

# Copy files
COPY ./build /build

# Build encoder4editing from source
RUN sudo git clone https://github.com/omertov/encoder4editing.git encoder4editing \
 && wget https://github.com/ninja-build/ninja/releases/download/v1.8.2/ninja-linux.zip \
 && unzip ninja-linux.zip -d /usr/local/bin/ \
 && update-alternatives --install /usr/bin/ninja ninja /usr/local/bin/ninja 1 --force \
 && rm -f ninja-linux.zip

# Build StyleCLIP from source
RUN git clone https://github.com/bycloudai/StyleCLIP \
 && cd StyleCLIP/global

WORKDIR /
RUN cp -r /build/copyfiles/afhqdog/ /StyleCLIP/global/npy/ \
 && cp -r /build/copyfiles/model/ /StyleCLIP/global/ \
 && cp -r /build/copyfiles/pretrained_models/ /encoder4editing/ \
 && cp -r /build/encoder4editing/* /encoder4editing/ \
 && cp -r /build/styleclip/* /StyleCLIP/global/ \
 && rm -rf /build

RUN mkdir -p /output \
 && mkdir -p /encoder4editing/latents
