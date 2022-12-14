FROM python:3.9-slim-buster

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "rest.py", "--port=8080"]