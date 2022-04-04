FROM ubuntu:focal

ADD packages.txt /tmp
ADD goimports.txt /tmp
ADD nodejs.list /etc/apt/sources.list.d
ADD nodesource.gpg.asc /etc/apt/trusted.gpg.d
ENV DEBIAN_FRONTEND noninteractive
ENV XDG_CACHE_HOME=/tmp/.cache

RUN apt-get update && grep '^[^ #]' /tmp/packages.txt        | \
        xargs apt-get install --yes --no-install-recommends && \
        rm -rf /var/lib/apt/lists/* /tmp/packages.txt

RUN wget https://go.dev/dl/go1.18.linux-amd64.tar.gz
RUN tar -xvf go1.18.linux-amd64.tar.gz
RUN mv go /usr/lib
ENV GOROOT /usr/lib/go
ENV GOPATH /go
ENV PATH $GOPATH/bin:$GOROOT/bin:$PATH

# RUN grep '^[^ #]' /tmp/goimports.txt | xargs go install && rm -rf /tmp/goimports.txt


# TODO: cambiar a $INPUT_PATH antes de correr $INPUT_COMMAND.
ENTRYPOINT ["/bin/sh", "-c"]
