# first stage contains complete development environment for gcc
FROM ubuntu:focal AS bld

RUN apt update \
    && apt install -y --no-install-recommends\
    gcc \
    libc6-dev \
    libc-dev-bin \
    libcrypt-dev \
    linux-libc-dev \
    manpages \
    manpages-dev \
    make \
    nano

# compile the code
WORKDIR /csource
COPY *.c .
COPY Makefile .
RUN make

# moving the executable to designated location
RUN mkdir -p /cbin \
    && mv main.out /cbin/


# the next stage is based on a pure base image
FROM ubuntu:focal

# just copy the completely linked executable
# we do not need gcc and all the dev libraries
COPY --from=bld /cbin /cbin
# make it available
ENV PATH=/cbin:$PATH
# run it as the main command of the container
CMD [ "main.out" ]
