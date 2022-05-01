FROM python:3.8

WORKDIR /WTW-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src ./src

COPY ./instance ./instance

COPY .flaskenv .

CMD ["flask", "run", "--host=0.0.0.0"]