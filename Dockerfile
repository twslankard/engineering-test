FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=python/web/app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers postgresql-dev zlib-dev jpeg-dev
COPY python/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]
