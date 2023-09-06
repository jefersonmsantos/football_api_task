FROM python:3.8-slim

COPY ./artifact /opt/artifact

RUN pip install -r /opt/artifact/requirements.txt

WORKDIR /opt/artifact

CMD ["python3","main.py"]