# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask","--app", "run.py", "run", "--host=0.0.0.0"]  