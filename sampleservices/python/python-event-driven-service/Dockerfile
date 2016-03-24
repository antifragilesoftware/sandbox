FROM python:3.5.1
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY microservice.py /usr/local/bin/microservice.py
ENTRYPOINT [ "python", "/usr/local/bin/microservice.py" ]