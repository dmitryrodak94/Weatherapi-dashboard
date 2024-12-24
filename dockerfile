FROM python:3.8.18


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

 
WORKDIR /app

COPY main.py main.py
ENTRYPOINT [ "python", "main.py" ]