FROM ubuntu:focal

ADD packages.txt /tmp
ADD goimports.txt /tmp
ADD nodejs.list /etc/apt/sources.list.d
ADD nodesource.gpg.asc /etc/apt/trusted.gpg.d
ENV DEBIAN_FRONTEND noninteractive
ENV XDG_CACHE_HOME=/tmp/.cache

ENV GOPATH /go
ENV PATH $GOPATH/bin:$PATH

RUN apt-get update && grep '^[^ #]' /tmp/packages.txt        | \
        xargs apt-get install --yes --no-install-recommends && \
        grep '^[^ #]' /tmp/goimports.txt | xargs go install && \
        rm -rf /var/lib/apt/lists/* /tmp/packages.txt /tmp/goimports.txt

# TODO: cambiar a $INPUT_PATH antes de correr $INPUT_COMMAND.
ENTRYPOINT ["/bin/sh", "-c"]
