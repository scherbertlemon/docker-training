FROM ubuntu:focal

LABEL maintainer="Rainer.Zufall@gmail.com"

ENV TZ=Europe/Berlin

RUN apt update \
	&& apt install \
	tzdata \
	--yes --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR	/wdir
# goes to wdir
COPY localfile.txt .

ENTRYPOINT [ "date" ]
# ENTRYPOINT [ "/bin/bash", "-c" ]
# CMD [ "date" ]
