FROM oraclelinux:8

RUN dnf -y update && \
    dnf -y upgrade

RUN dnf install python39 -y &&\
    dnf install python39-pip -y && \
    python3 -m pip install pipenv

COPY src/ /app/

COPY Pipfile* /app/

WORKDIR /app/

RUN pipenv install --ignore-pipfile --system

ENTRYPOINT ["python3"]

CMD ["server.py"]
