FROM ubuntu:focal

LABEL maintainer="somebody@somewhere.com"

ARG MCONDA_DL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
ARG CONDA_PATH=/opt/miniconda

ENV TZ=Europe/Berlin
ENV SHELL=/bin/bash
ENV PATH=${CONDA_PATH}/bin:$PATH

WORKDIR /pysource

RUN apt update \
    && apt install wget python tzdata ca-certificates -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p ${CONDA_PATH}

RUN wget ${MCONDA_DL}

RUN ${SHELL} $(basename ${MCONDA_DL}) -f -b -p ${CONDA_PATH} \
    && rm $(basename ${MCONDA_DL})

COPY requirements.txt .
RUN conda install -n base --file requirements.txt --yes \
    && conda clean --all --yes

COPY greeting.py .

CMD ["conda", "run", "--no-capture-output", "-n", "base", "python", "greeting.py"]

