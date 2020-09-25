# -*- docker-image-name: "algoritmosrw/corrector" -*-

FROM algoritmosrw/corrector:v3

COPY ["*.py", "*.j2", "/"]

USER nobody
WORKDIR /tmp

ENTRYPOINT ["/worker.py"]

# vi:et
