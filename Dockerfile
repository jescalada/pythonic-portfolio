FROM python:3.9-slim-buster

WORKDIR /pythonic-portfolio

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]

EXPOSE 80
